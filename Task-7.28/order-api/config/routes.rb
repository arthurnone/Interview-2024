Rails.application.routes.draw do
  root to: redirect('/products')
  resources :products, defaults: { format: :json }, only: [:index, :show]
  resources :orders, defaults: { format: :json }
end
