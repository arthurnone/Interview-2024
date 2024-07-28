class CreateOrders < ActiveRecord::Migration[7.1]
  def change
    create_table :orders, id: false do |t|
      t.string :id, primary_key: true, null: false, default: -> { "LOWER(HEX(RANDOMBLOB(4))) || '-' || LOWER(HEX(RANDOMBLOB(2))) || '-4' || SUBSTR(LOWER(HEX(RANDOMBLOB(2))),2) || '-' || SUBSTR('89ab', 1 + (ABS(RANDOM()) % 4) , 1) || SUBSTR(LOWER(HEX(RANDOMBLOB(2))),2) || '-' || LOWER(HEX(RANDOMBLOB(6)))" }
      t.references :product, null: false, foreign_key: true
      t.integer :quantity
      t.decimal :total_price
      t.string :user_id
      t.string :status, null: true  

      t.timestamps
    end
  end
end
