import React from 'react';

const Footer = () => {
  return (
    <footer className="bg-secondary text-white py-6 mt-10">
      <div className="container mx-auto flex flex-col items-center">
        <div className="text-center mb-4">
          <p>Copyright © 2024 Peifeng Wang Lab.</p>
        </div>
        <div className="text-center mb-4">
          <p>
            Email:
            <a href="mailto:root@wangpeifeng.com" className="text-blue-400">
              root@wangpeifeng.com
            </a>
          </p>
          <p>
            My Website:
            <a href="https://wangpeifeng.com/" className="text-blue-400">
              wangpeifeng.com
            </a>
          </p>
        </div>
        <div className="text-center">
          <p>Thanks for visiting!</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
