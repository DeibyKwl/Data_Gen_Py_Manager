import generated_data.generate_store as store_gen
import generated_data.generate_game as game_gen

# Generate 1000 fake stores and 5000 fake games that will be linked to a store.
store_gen.generate_and_write_stores(1000)
game_gen.generate_and_write_games(5000)