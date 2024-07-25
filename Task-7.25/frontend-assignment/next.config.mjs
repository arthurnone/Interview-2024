/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    domains: ['i.pravatar.cc'],
  },
};

if (process.env.NODE_ENV === 'production') {
  nextConfig.output = 'export';
}

export default nextConfig;
