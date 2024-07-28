require 'test_helper'

class ProductsControllerTest < ActionDispatch::IntegrationTest
  setup do
    @product = products(:one) # Assuming you have a fixture for products
  end

  test "should get index" do
    get products_url, as: :json
    assert_response :success
    assert_equal "success", JSON.parse(response.body)["status"]
  end

  test "should show product" do
    get product_url(@product), as: :json
    assert_response :success
  end

end
