export default function Footer() {
  return (
    <footer className="w-full bg-gray-900 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="flex flex-col items-center justify-center space-y-6">
          {/* CTA 버튼 */}
          <div>
            <button className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-md shadow-md">
              문의하기
            </button>
          </div>

          {/* 저작권 표시 */}
          <div className="text-center">
            <p className="text-gray-400 text-sm">
              &copy; {new Date().getFullYear()} My Awesome Site. All rights reserved.
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
}
