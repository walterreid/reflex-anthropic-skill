# Recipe — Generate a Complete Recipe

Generate a well-structured, tested-style recipe for a given dish using the recipe display widget.

- **Dish**: {dish}
- **Style**: {style}
- **Servings**: {servings}

## Instructions

1. If `{style}` is provided, tailor the recipe to that cuisine or approach (e.g., “Italian grandma”, “quick weeknight”, “restaurant-quality”). Otherwise, default to a classic, well-regarded version.
1. Use the `recipe_display_v0` tool to present the recipe as an interactive widget with:
- A descriptive title
- Brief description capturing the dish’s character
- Complete ingredient list with proper units and amounts scaled to `{servings}` servings
- Clear, ordered steps with timers where applicable
- Helpful notes covering tips, variations, and make-ahead advice
1. Prioritize flavor-building techniques (proper seasoning, layering, resting times) over shortcuts.
1. Include all sub-components (sauces, doughs, toppings) as part of the single recipe flow.

## Output

An interactive recipe widget rendered via `recipe_display_v0`. No additional prose beyond a one-sentence intro.