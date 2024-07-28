class OrdersController < ApplicationController
  ALLOWED_STATUSES = ["Pending", "Processing", "Complete", "Closed", "Cancelled"]
  skip_before_action :verify_authenticity_token, only: [:create, :update, :destroy]
  before_action :set_order, only: %i[ show update destroy ]

  # GET /orders
  def index
    page = (params[:page] || 1).to_i
    limit = (params[:limit] || 10).to_i
    status = params[:status]
    sort = params[:sort] || 'created_at'
    offset = (page - 1) * limit

    if status.present?
      total = Order.where(status: status).count
      @orders = Order.where(status: status)
                     .order(sort)
                     .offset(offset)
                     .limit(limit)
    else
      total = Order.count
      @orders = Order.order(sort)
                     .offset(offset)
                     .limit(limit)
    end

    render json: { 
      status: "success",
      page: page,
      total: total,
      limit: limit,
      orders: @orders 
    }, status: :ok
  end

  # GET /orders/1
  def show
    render json: @order
  end

  # POST /orders
  def create
    @order = Order.new(order_params)
    @order.user_id = "test_user"
    @order.status = "Pending"
  
    # Calculate the total price based on product price and quantity
    if @order.quantity.present? && @order.product.present?
      @order.total_price = @order.product.price * @order.quantity
    end
  
    if @order.save
      render json: @order, status: :created, location: @order
    else
      render json: @order.errors, status: :unprocessable_entity
    end
  end

  # PATCH/PUT /orders/1
  def update
    raw_body = request.body.read
    request_body_json = JSON.parse(raw_body) rescue {}
  
    # Ensure only orders with status 'Pending' can be updated
    if @order.status != 'Pending'
      render json: { error: 'Only orders with status Pending can be updated' }, status: :unprocessable_entity
      return
    end
  
    # Ensure only 'quantity' can be updated
    request_body_json = request_body_json.slice('quantity')
  
    # If 'quantity' is present, calculate the 'total_price'
    if request_body_json.key?('quantity')
      product_price = @order.product.price
      request_body_json['total_price'] = product_price * request_body_json['quantity']
    end
  
    if @order.update(request_body_json)
      render json: @order
    else
      render json: @order.errors, status: :unprocessable_entity
    end
  end

  # DELETE /orders/1
  def destroy
    @order.destroy
    head :no_content
  end

  private
    # Use callbacks to share common setup or constraints between actions.
    def set_order
      @order = Order.find(params[:id])
    end

    # Only allow a list of trusted parameters through.
    def order_params
      params.require(:order).permit(:product_id, :quantity)
    end
end
