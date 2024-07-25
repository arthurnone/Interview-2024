let API_BASE_URL: string;
if (process.env.NODE_ENV === 'production') {
  API_BASE_URL = '';
} else {
  API_BASE_URL = 'http://127.0.0.1:10001/';
}

export { API_BASE_URL };
