class ProductsController < ApplicationController
  before_action :set_product, only: %i[ show update destroy ]

  def index
    page = (params[:page] || 1).to_i
    limit = (params[:limit] || 10).to_i
    sort = params[:sort] || 'id'
    offset = (page - 1) * limit
    total = Product.count

    @products = Product.order(sort)
                       .offset(offset)
                       .limit(limit)

    render json: { 
      status: "success",
      page: page,
      total: total,
      limit: limit,
      products: @products 
    }, status: :ok

  rescue JSON::ParserError => e
    Rails.logger.error "Failed to parse JSON: #{e.message}"
    render json: { error: "Invalid JSON format" }, status: :bad_request
  end

  # GET /products/1
  def show
    render json: @product
  end

  # POST /products
  def create
  end

  # PATCH/PUT /products/1
  def update
  end

  # DELETE /products/1
  def destroy
  end

  private

    def set_product
      @product = Product.find(params[:id])
    end

    def product_params
      params.require(:product).permit(:name, :price, :description)
    end
end
