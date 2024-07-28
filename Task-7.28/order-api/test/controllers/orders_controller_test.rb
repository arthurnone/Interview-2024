require 'test_helper'

class OrdersControllerTest < ActionDispatch::IntegrationTest
  setup do
    @order = orders(:one) # Assuming you have a fixture for orders
    @product = products(:one)
  end

  test "should get index" do
    get orders_url, as: :json
    assert_response :success
    assert_equal "success", JSON.parse(response.body)["status"]
  end

  test "should show order" do
    get order_url(@order), as: :json
    assert_response :success
  end

  test "should create order" do
    assert_difference('Order.count') do
      post orders_url, params: { order: { product_id: @product.id, quantity: 2, total_price: 39.98 } }, as: :json
    end
  
    assert_response :created
  end

  test "should update order" do
    patch order_url(@order), params: { quantity: 10 }, as: :json
    assert_response :success
  end

  test "should destroy order" do
    assert_difference('Order.count', -1) do
      delete order_url(@order), as: :json
    end

    assert_response :no_content
  end
end
