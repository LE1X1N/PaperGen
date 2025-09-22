import React from 'react';

function App() {
  return (
    <div className="w-[375px] h-[667px] border-4 border-black bg-white flex flex-col mx-auto rounded-3xl overflow-hidden">
      {/* 状态栏 */}
      <div className="flex justify-between items-center px-5 py-3 text-xs text-black bg-white">
        <div className="flex items-center gap-2">
          <span className="text-[11px]">●●●●●</span>
          <span>WeChat</span>
        </div>
        {/* 时间 */}
        <span className="text-sm">20:35</span>
        {/* 电池 */}
        <div className="flex items-center gap-1">
          <div className="relative flex items-center">
            <div className="w-8 h-4 border-2 border-black rounded-sm flex items-center px-[2px]">
              <div className="h-2.5 bg-black rounded-sm" style={{ width: '80%' }} />
            </div>
          </div>
          <span className="text-sm">80%</span>
        </div>
      </div>

      {/* 标题栏 */}
      <div className="flex justify-between items-center px-3 py-2 border-b bg-white">
        {/* 返回箭头 */}
        <button className="w-8 h-8 flex items-center justify-center rounded-md hover:bg-gray-100">
          <svg
            width="18"
            height="18"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M15 6 L9 12 L15 18"
              stroke="#111"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              fill="none"
            />
          </svg>
        </button>

        {/* 中间标题 */}
        <div className="text-base font-medium">功能1</div>

        {/* 右上椭圆容器 */}
        <div className="flex items-center gap-2 px-2 py-1 border border-gray-200 rounded-full shadow-sm bg-white">
          {/* 三个点 */}
          <svg
            width="36"
            height="14"
            viewBox="0 0 36 14"
            xmlns="http://www.w3.org/2000/svg"
          >
            <circle cx="6" cy="7" r="2.6" fill="#111" />
            <circle cx="18" cy="7" r="4.3" fill="#111" />
            <circle cx="30" cy="7" r="2.6" fill="#111" />
          </svg>

          {/* 圆圈 + 中心点 */}
          <svg
            width="28"
            height="28"
            viewBox="0 0 28 28"
            xmlns="http://www.w3.org/2000/svg"
          >
            <circle cx="14" cy="14" r="9.2" stroke="#111" strokeWidth="2.6" fill="none" />
            <circle cx="14" cy="14" r="3.6" fill="#111" />
          </svg>
        </div>
      </div>

      {/* 主体内容占位 */}
      <main className="flex-1 bg-gray-50 flex items-center justify-center">
        {/* 这里放你的内容 */}
        <div className="flex flex-col items-center gap-4">
          <span className="text-gray-400">页面内容区域</span>

          
        </div>
      </main>
    </div>
  );
}
export default App;