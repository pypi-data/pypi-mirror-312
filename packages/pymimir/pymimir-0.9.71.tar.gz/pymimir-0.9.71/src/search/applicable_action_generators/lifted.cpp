/*
 * Copyright (C) 2023 Dominik Drexler and Simon Stahlberg
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program. If not, see <https://www.gnu.org/licenses/>.
 */

#include "mimir/search/applicable_action_generators/lifted.hpp"

#include "mimir/common/itertools.hpp"
#include "mimir/formalism/action.hpp"
#include "mimir/formalism/literal.hpp"
#include "mimir/formalism/object.hpp"
#include "mimir/formalism/predicate_tag.hpp"
#include "mimir/formalism/repositories.hpp"
#include "mimir/formalism/utils.hpp"
#include "mimir/formalism/variable.hpp"
#include "mimir/search/action.hpp"
#include "mimir/search/applicable_action_generators/lifted/consistency_graph.hpp"
#include "mimir/search/condition_grounders.hpp"

#include <boost/dynamic_bitset.hpp>
#include <stdexcept>
#include <vector>

using namespace std::string_literals;

namespace mimir
{

class GroundAndEvaluateFunctionExpressionVisitor
{
private:
    const GroundFunctionToValue& m_ground_function_to_cost;
    const ObjectList& m_binding;
    PDDLRepositories& m_pddl_repositories;

    GroundFunction ground_function(const Function& function)
    {
        auto grounded_terms = ObjectList {};
        m_pddl_repositories.ground_variables(function->get_terms(), m_binding, grounded_terms);
        return m_pddl_repositories.get_or_create_ground_function(function->get_function_skeleton(), grounded_terms);
    }

public:
    GroundAndEvaluateFunctionExpressionVisitor(const GroundFunctionToValue& ground_function_value_cost,
                                               const ObjectList& binding,
                                               PDDLRepositories& ref_pddl_repositories) :

        m_ground_function_to_cost(ground_function_value_cost),
        m_binding(binding),
        m_pddl_repositories(ref_pddl_repositories)
    {
    }

    double operator()(const FunctionExpressionImpl& expr)
    {
        return std::visit([this](auto&& arg) -> double { return (*this)(*arg); }, expr.get_variant());
    }

    double operator()(const FunctionExpressionNumberImpl& expr) { return expr.get_number(); }

    double operator()(const FunctionExpressionBinaryOperatorImpl& expr)
    {
        return evaluate_binary(expr.get_binary_operator(), (*this)(*expr.get_left_function_expression()), (*this)(*expr.get_right_function_expression()));
    }

    double operator()(const FunctionExpressionMultiOperatorImpl& expr)
    {
        assert(!expr.get_function_expressions().empty());

        auto result = ContinuousCost(0);
        for (const auto& child_expr : expr.get_function_expressions())
        {
            result = evaluate_multi(expr.get_multi_operator(), result, (*this)(*child_expr));
        }

        return result;
    }

    double operator()(const FunctionExpressionMinusImpl& expr) { return -(*this)(*expr.get_function_expression()); }

    double operator()(const FunctionExpressionFunctionImpl& expr)
    {
        auto grounded_function = ground_function(expr.get_function());

        auto it = m_ground_function_to_cost.find(grounded_function);
        if (it == m_ground_function_to_cost.end())
        {
            throw std::runtime_error("No numeric fluent available to determine cost for ground function "s + grounded_function->str());
        }
        const auto cost = it->second;

        return cost;
    }
};

const std::vector<AxiomPartition>& LiftedApplicableActionGenerator::get_axiom_partitioning() const { return m_axiom_evaluator.get_axiom_partitioning(); }

GroundAxiom LiftedApplicableActionGenerator::ground_axiom(Axiom axiom, ObjectList&& binding)
{
    return m_axiom_evaluator.ground_axiom(axiom, std::move(binding));
}

GroundAction LiftedApplicableActionGenerator::ground_action(Action action, ObjectList&& binding)
{
    /* 1. Check if grounding is cached */

    auto& groundings = m_action_groundings[action];
    auto it = groundings.find(binding);
    if (it != groundings.end())
    {
        m_event_handler->on_ground_action_cache_hit(action, binding);

        return it->second;
    }

    m_event_handler->on_ground_action_cache_miss(action, binding);

    /* 2. Ground the action */

    m_event_handler->on_ground_action(action, binding);

    const auto fill_effects = [this](const LiteralList<Fluent>& literals, SimpleFluentEffectList& out_effects, const auto& binding)
    {
        out_effects.clear();

        for (const auto& literal : literals)
        {
            const auto grounded_literal = m_pddl_repositories->ground_literal(literal, binding);
            out_effects.emplace_back(grounded_literal->is_negated(), grounded_literal->get_atom()->get_index());
        }
    };

    /* Header */

    m_action_builder.get_index() = m_flat_actions.size();
    m_action_builder.get_action_index() = action->get_index();
    auto& objects = m_action_builder.get_objects();
    objects.clear();
    for (const auto& obj : binding)
    {
        objects.push_back(obj->get_index());
    }

    /* Precondition */
    auto& strips_precondition = m_action_builder.get_strips_precondition();
    auto& positive_fluent_precondition = strips_precondition.get_positive_precondition<Fluent>();
    auto& negative_fluent_precondition = strips_precondition.get_negative_precondition<Fluent>();
    auto& positive_static_precondition = strips_precondition.get_positive_precondition<Static>();
    auto& negative_static_precondition = strips_precondition.get_negative_precondition<Static>();
    auto& positive_derived_precondition = strips_precondition.get_positive_precondition<Derived>();
    auto& negative_derived_precondition = strips_precondition.get_negative_precondition<Derived>();
    positive_fluent_precondition.unset_all();
    negative_fluent_precondition.unset_all();
    positive_static_precondition.unset_all();
    negative_static_precondition.unset_all();
    positive_derived_precondition.unset_all();
    negative_derived_precondition.unset_all();
    m_pddl_repositories->ground_and_fill_bitset(action->get_conditions<Fluent>(), positive_fluent_precondition, negative_fluent_precondition, binding);
    m_pddl_repositories->ground_and_fill_bitset(action->get_conditions<Static>(), positive_static_precondition, negative_static_precondition, binding);
    m_pddl_repositories->ground_and_fill_bitset(action->get_conditions<Derived>(), positive_derived_precondition, negative_derived_precondition, binding);

    /* Simple effects */
    auto& strips_effect = m_action_builder.get_strips_effect();
    auto& positive_effect = strips_effect.get_positive_effects();
    auto& negative_effect = strips_effect.get_negative_effects();
    positive_effect.unset_all();
    negative_effect.unset_all();
    const auto& effect_literals = action->get_simple_effects()->get_effect();
    m_pddl_repositories->ground_and_fill_bitset(effect_literals, positive_effect, negative_effect, binding);
    strips_effect.get_cost() = GroundAndEvaluateFunctionExpressionVisitor(m_ground_function_to_cost, binding, *m_pddl_repositories)(
        *action->get_simple_effects()->get_function_expression());

    /* Conditional effects */
    // Fetch data
    auto& conditional_effects = m_action_builder.get_conditional_effects();
    // TODO: Unfortunately, this unnecessary causes deallocations. We need to write a custom cista vector that avoids this.
    conditional_effects.clear();

    // Resize builders.
    /* Universal effects */

    // We have copy the binding to extend it with objects for quantified effect variables
    // and at the same time we need to use the original binding as cache key.
    auto binding_ext = binding;

    const auto num_complex_effects = action->get_complex_effects().size();
    if (num_complex_effects > 0)
    {
        const auto& complex_effect_consistency_graphs = m_action_complex_effects.at(action);
        const auto binding_ext_size = binding_ext.size();
        for (size_t i = 0; i < num_complex_effects; ++i)
        {
            // Fetch data
            const auto& complex_effect = action->get_complex_effects().at(i);

            // Resize builders.
            if (complex_effect->get_arity() > 0)
            {
                const auto& consistency_graph = complex_effect_consistency_graphs.at(i);
                const auto& objects_by_parameter_index = consistency_graph.get_objects_by_parameter_index();

                const auto num_conditional_effects = CartesianProduct(objects_by_parameter_index).num_combinations();
                const auto old_size = conditional_effects.size();
                conditional_effects.resize(old_size + num_conditional_effects);

                // Create binding and ground conditions and effect
                binding_ext.resize(binding_ext_size + complex_effect->get_arity());

                // The position to place the conditional precondition + effect
                auto j = old_size;
                assert(!objects_by_parameter_index.empty());
                for (const auto& combination : CartesianProduct(objects_by_parameter_index))
                {
                    // Create binding
                    for (size_t pos = 0; pos < complex_effect->get_arity(); ++pos)
                    {
                        const auto object_index = *combination[pos];
                        binding_ext[binding_ext_size + pos] = m_pddl_repositories->get_object(object_index);
                    }

                    auto& cond_effect_j = conditional_effects[j];
                    auto& cond_positive_fluent_precondition_j = cond_effect_j.get_positive_precondition<Fluent>();
                    auto& cond_negative_fluent_precondition_j = cond_effect_j.get_negative_precondition<Fluent>();
                    auto& cond_positive_static_precondition_j = cond_effect_j.get_positive_precondition<Static>();
                    auto& cond_negative_static_precondition_j = cond_effect_j.get_negative_precondition<Static>();
                    auto& cond_positive_derived_precondition_j = cond_effect_j.get_positive_precondition<Derived>();
                    auto& cond_negative_derived_precondition_j = cond_effect_j.get_negative_precondition<Derived>();
                    auto& cond_simple_effect_j = cond_effect_j.get_simple_effect();
                    cond_positive_fluent_precondition_j.clear();
                    cond_negative_fluent_precondition_j.clear();
                    cond_positive_static_precondition_j.clear();
                    cond_negative_static_precondition_j.clear();
                    cond_positive_derived_precondition_j.clear();
                    cond_negative_derived_precondition_j.clear();
                    m_pddl_repositories->ground_and_fill_vector(complex_effect->get_conditions<Fluent>(),
                                                                cond_positive_fluent_precondition_j,
                                                                cond_negative_fluent_precondition_j,
                                                                binding_ext);
                    m_pddl_repositories->ground_and_fill_vector(complex_effect->get_conditions<Static>(),
                                                                cond_positive_static_precondition_j,
                                                                cond_negative_static_precondition_j,
                                                                binding_ext);
                    m_pddl_repositories->ground_and_fill_vector(complex_effect->get_conditions<Derived>(),
                                                                cond_positive_derived_precondition_j,
                                                                cond_negative_derived_precondition_j,
                                                                binding_ext);

                    fill_effects(complex_effect->get_effect(), cond_simple_effect_j, binding_ext);

                    cond_effect_j.get_cost() = GroundAndEvaluateFunctionExpressionVisitor(m_ground_function_to_cost, binding, *m_pddl_repositories)(
                        *complex_effect->get_function_expression());

                    ++j;
                }
            }
            else
            {
                conditional_effects.resize(conditional_effects.size() + 1);
                auto& cond_effect = conditional_effects.back();
                auto& cond_positive_fluent_precondition = cond_effect.get_positive_precondition<Fluent>();
                auto& cond_negative_fluent_precondition = cond_effect.get_negative_precondition<Fluent>();
                auto& cond_positive_static_precondition = cond_effect.get_positive_precondition<Static>();
                auto& cond_negative_static_precondition = cond_effect.get_negative_precondition<Static>();
                auto& cond_positive_derived_precondition = cond_effect.get_positive_precondition<Derived>();
                auto& cond_negative_derived_precondition = cond_effect.get_negative_precondition<Derived>();
                auto& cond_simple_effect = cond_effect.get_simple_effect();
                cond_positive_fluent_precondition.clear();
                cond_negative_fluent_precondition.clear();
                cond_positive_static_precondition.clear();
                cond_negative_static_precondition.clear();
                cond_positive_derived_precondition.clear();
                cond_negative_derived_precondition.clear();
                m_pddl_repositories->ground_and_fill_vector(complex_effect->get_conditions<Fluent>(),
                                                            cond_positive_fluent_precondition,
                                                            cond_negative_fluent_precondition,
                                                            binding);
                m_pddl_repositories->ground_and_fill_vector(complex_effect->get_conditions<Static>(),
                                                            cond_positive_static_precondition,
                                                            cond_negative_static_precondition,
                                                            binding);
                m_pddl_repositories->ground_and_fill_vector(complex_effect->get_conditions<Derived>(),
                                                            cond_positive_derived_precondition,
                                                            cond_negative_derived_precondition,
                                                            binding);

                fill_effects(complex_effect->get_effect(), cond_simple_effect, binding);

                cond_effect.get_cost() = GroundAndEvaluateFunctionExpressionVisitor(m_ground_function_to_cost, binding, *m_pddl_repositories)(
                    *complex_effect->get_function_expression());
            }
        }
    }

    const auto [iter, inserted] = m_flat_actions.insert(m_action_builder);
    const auto grounded_action = *iter;
    if (inserted)
    {
        m_actions_by_index.push_back(grounded_action);
    }

    /* 3. Insert to groundings table */

    groundings.emplace(std::move(binding), GroundAction(grounded_action));

    /* 4. Return the resulting ground action */

    return grounded_action;
}

void LiftedApplicableActionGenerator::generate_applicable_actions(State state, GroundActionList& out_applicable_actions)
{
    out_applicable_actions.clear();

    m_event_handler->on_start_generating_applicable_actions();

    // Create the assignment sets that are shared by all action schemas.

    auto& fluent_predicates = m_problem->get_domain()->get_predicates<Fluent>();
    auto fluent_atoms = m_pddl_repositories->get_ground_atoms_from_indices<Fluent>(state->get_atoms<Fluent>());

    auto fluent_assignment_set = AssignmentSet<Fluent>(m_problem, fluent_predicates, fluent_atoms);

    auto& derived_predicates = m_problem->get_problem_and_domain_derived_predicates();

    auto derived_atoms = m_pddl_repositories->get_ground_atoms_from_indices<Derived>(state->get_atoms<Derived>());
    auto derived_assignment_set = AssignmentSet<Derived>(m_problem, derived_predicates, derived_atoms);

    // Get all applicable ground actions.
    // This is done by getting bindings in the given state using the precondition.
    // These bindings are then used to ground the actual action schemas.

    std::vector<ObjectList> bindings;
    for (auto& [action, condition_grounder] : m_action_precondition_grounders)
    {
        condition_grounder.compute_bindings(state, fluent_assignment_set, derived_assignment_set, bindings);

        for (auto& binding : bindings)
        {
            out_applicable_actions.emplace_back(ground_action(action, std::move(binding)));
        }
    }

    m_event_handler->on_end_generating_applicable_actions(out_applicable_actions, *m_pddl_repositories);
}

void LiftedApplicableActionGenerator::generate_and_apply_axioms(StateImpl& unextended_state)
{
    // In the lifted case, we use the axiom evaluator.
    m_axiom_evaluator.generate_and_apply_axioms(unextended_state);
}

void LiftedApplicableActionGenerator::on_finish_search_layer() const { m_event_handler->on_finish_search_layer(); }

void LiftedApplicableActionGenerator::on_end_search() const { m_event_handler->on_end_search(); }

LiftedApplicableActionGenerator::LiftedApplicableActionGenerator(Problem problem, std::shared_ptr<PDDLRepositories> pddl_repositories) :
    LiftedApplicableActionGenerator(problem, std::move(pddl_repositories), std::make_shared<DefaultLiftedApplicableActionGeneratorEventHandler>())
{
}

LiftedApplicableActionGenerator::LiftedApplicableActionGenerator(Problem problem,
                                                                 std::shared_ptr<PDDLRepositories> pddl_repositories,
                                                                 std::shared_ptr<ILiftedApplicableActionGeneratorEventHandler> event_handler) :
    m_problem(problem),
    m_pddl_repositories(std::move(pddl_repositories)),
    m_event_handler(std::move(event_handler)),
    m_axiom_evaluator(problem, m_pddl_repositories, m_event_handler),
    m_action_precondition_grounders(),
    m_action_complex_effects(),
    m_ground_function_to_cost()
{
    /* 1. Initialize ground function costs. */

    for (const auto numeric_fluent : problem->get_numeric_fluents())
    {
        m_ground_function_to_cost.emplace(numeric_fluent->get_function(), numeric_fluent->get_number());
    }

    /* 2. Initialize the condition grounders for each action schema. */

    auto static_initial_atoms = to_ground_atoms(m_problem->get_static_initial_literals());
    auto static_assignment_set = AssignmentSet<Static>(m_problem, m_problem->get_domain()->get_predicates<Static>(), static_initial_atoms);

    for (const auto& action : m_problem->get_domain()->get_actions())
    {
        m_action_precondition_grounders.emplace(action,
                                                ConditionGrounder(m_problem,
                                                                  action->get_parameters(),
                                                                  action->get_conditions<Static>(),
                                                                  action->get_conditions<Fluent>(),
                                                                  action->get_conditions<Derived>(),
                                                                  static_assignment_set,
                                                                  m_pddl_repositories));
        auto complex_effects = std::vector<consistency_graph::StaticConsistencyGraph>();
        complex_effects.reserve(action->get_complex_effects().size());

        for (const auto& complex_effect : action->get_complex_effects())
        {
            complex_effects.push_back(consistency_graph::StaticConsistencyGraph(problem,
                                                                                action->get_arity(),
                                                                                action->get_arity() + complex_effect->get_arity(),
                                                                                complex_effect->get_conditions<Static>(),
                                                                                static_assignment_set));
        }

        m_action_complex_effects.emplace(action, std::move(complex_effects));
    }
}

const GroundActionList& LiftedApplicableActionGenerator::get_ground_actions() const { return m_actions_by_index; }

GroundAction LiftedApplicableActionGenerator::get_ground_action(Index action_index) const { return m_actions_by_index.at(action_index); }

const GroundAxiomList& LiftedApplicableActionGenerator::get_ground_axioms() const { return m_axiom_evaluator.get_ground_axioms(); }

GroundAxiom LiftedApplicableActionGenerator::get_ground_axiom(Index axiom_index) const { return m_axiom_evaluator.get_ground_axiom(axiom_index); }

size_t LiftedApplicableActionGenerator::get_num_ground_actions() const { return m_actions_by_index.size(); }

size_t LiftedApplicableActionGenerator::get_num_ground_axioms() const { return m_axiom_evaluator.get_num_ground_axioms(); }

Problem LiftedApplicableActionGenerator::get_problem() const { return m_problem; }

const std::shared_ptr<PDDLRepositories>& LiftedApplicableActionGenerator::get_pddl_repositories() const { return m_pddl_repositories; }

std::ostream& operator<<(std::ostream& out, const LiftedApplicableActionGenerator& lifted_applicable_action_generator)
{
    out << "Lifted AAG:" << std::endl;

    for (const auto& [action, grounder] : lifted_applicable_action_generator.m_action_precondition_grounders)
    {
        out << " - Action: " << action->get_name() << std::endl;
        out << grounder << std::endl;
    }

    return out;
}

}
