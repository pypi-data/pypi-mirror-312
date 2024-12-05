# sage_setup: distribution = sagemath-categories
r"""
Complex reflection groups
"""
#*****************************************************************************
#       Copyright (C) 2011-2015 Christian Stump <christian.stump at gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#                  http://www.gnu.org/licenses/
#*****************************************************************************

from sage.misc.cachefunc import cached_method
from sage.misc.lazy_import import LazyImport
from sage.categories.category_singleton import Category_singleton
from sage.categories.complex_reflection_or_generalized_coxeter_groups import ComplexReflectionOrGeneralizedCoxeterGroups


class ComplexReflectionGroups(Category_singleton):
    r"""
    The category of complex reflection groups.

    Let `V` be a complex vector space. A *complex reflection* is an
    element of `\operatorname{GL}(V)` fixing a hyperplane pointwise
    and acting by multiplication by a root of unity on a complementary
    line.

    A *complex reflection group* is a group `W` that is (isomorphic
    to) a subgroup of some general linear group `\operatorname{GL}(V)`
    generated by a distinguished set of complex reflections.

    The dimension of `V` is the *rank* of `W`.

    For a comprehensive treatment of complex reflection groups and
    many definitions and theorems used here, we refer to [LT2009]_.
    See also :wikipedia:`Reflection_group`.

    .. SEEALSO::

        :func:`ReflectionGroup` for usage examples of this category.

    EXAMPLES::

        sage: from sage.categories.complex_reflection_groups import ComplexReflectionGroups
        sage: ComplexReflectionGroups()
        Category of complex reflection groups
        sage: ComplexReflectionGroups().super_categories()
        [Category of complex reflection or generalized Coxeter groups]
        sage: ComplexReflectionGroups().all_super_categories()
        [Category of complex reflection groups,
         Category of complex reflection or generalized Coxeter groups,
         Category of groups,
         Category of monoids,
         Category of finitely generated semigroups,
         Category of semigroups,
         Category of finitely generated magmas,
         Category of inverse unital magmas,
         Category of unital magmas,
         Category of magmas,
         Category of enumerated sets,
         Category of sets,
         Category of sets with partial maps,
         Category of objects]

    An example of a reflection group::

        sage: W = ComplexReflectionGroups().example(); W                                # needs sage.combinat
        5-colored permutations of size 3

    ``W`` is in the category of complex reflection groups::

        sage: W in ComplexReflectionGroups()                                            # needs sage.combinat
        True

    TESTS::

        sage: TestSuite(W).run()                                                        # needs sage.combinat
        sage: TestSuite(ComplexReflectionGroups()).run()
    """

    @cached_method
    def super_categories(self):
        r"""
        Return the super categories of ``self``.

        EXAMPLES::

            sage: from sage.categories.complex_reflection_groups import ComplexReflectionGroups
            sage: ComplexReflectionGroups().super_categories()
            [Category of complex reflection or generalized Coxeter groups]
        """
        return [ComplexReflectionOrGeneralizedCoxeterGroups()]

    def additional_structure(self):
        r"""
        Return ``None``.

        Indeed, all the structure complex reflection groups have in
        addition to groups (simple reflections, ...) is already
        defined in the super category.

        .. SEEALSO:: :meth:`Category.additional_structure`

        EXAMPLES::

            sage: from sage.categories.complex_reflection_groups import ComplexReflectionGroups
            sage: ComplexReflectionGroups().additional_structure()
        """
        return None

    def example(self):
        r"""
        Return an example of a complex reflection group.

        EXAMPLES::

            sage: from sage.categories.complex_reflection_groups import ComplexReflectionGroups
            sage: ComplexReflectionGroups().example()                                   # needs sage.combinat
            5-colored permutations of size 3
        """
        from sage.combinat.colored_permutations import ColoredPermutations
        return ColoredPermutations(5, 3)

    class ParentMethods:

        @cached_method
        def rank(self):
            r"""
            Return the rank of ``self``.

            The rank of ``self`` is the dimension of the smallest
            faithfull reflection representation of ``self``.

            EXAMPLES::

                sage: W = CoxeterGroups().example(); W
                The symmetric group on {0, ..., 3}
                sage: W.rank()
                3
            """

    Finite = LazyImport('sage.categories.finite_complex_reflection_groups',
                        'FiniteComplexReflectionGroups', as_name='Finite')
