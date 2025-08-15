import React from "react";

export default function App() {
  return (
    <div className="flex h-screen font-['PingFang SC',sans-serif] text-gray-900 bg-gradient-to-r from-yellow-50 via-yellow-100 to-yellow-50">
      {/* 侧边栏 */}
      <aside className="flex flex-col w-72 bg-yellow-400 shadow-xl">
        <div className="flex items-center justify-center h-20 border-b border-yellow-300">
          <h2 className="text-3xl font-extrabold text-white tracking-widest">
            管理系统
          </h2>
        </div>
        <nav className="flex flex-col flex-grow px-8 py-10 space-y-6">
          {[
            { name: "仪表盘", icon: "⬛" },
            { name: "报告", icon: "📊" },
            { name: "用户", icon: "👥" },
            { name: "设置", icon: "⚙️" },
          ].map((item) => (
            <a
              key={item.name}
              href="#"
              className="flex items-center space-x-4 px-5 py-3 rounded-lg bg-yellow-300 text-yellow-900 font-semibold shadow-inner transition-transform transform hover:scale-105 hover:bg-yellow-350 active:scale-95"
              draggable={false}
            >
              <span className="text-xl select-none">{item.icon}</span>
              <span>{item.name}</span>
            </a>
          ))}

          <div className="mt-auto">
            <a
              href="#"
              className="block w-full text-center px-5 py-3 font-semibold rounded-lg bg-yellow-500 text-white shadow-lg hover:bg-yellow-600 transition"
            >
              登出
            </a>
          </div>
        </nav>
      </aside>

      {/* 主内容 */}
      <main className="flex flex-col flex-grow overflow-auto">
        {/* 顶部 */}
        <header className="flex items-center justify-between bg-white shadow-md h-16 px-10 border-b border-yellow-200">
          <h1 className="text-2xl font-bold tracking-wide text-yellow-800 select-none">
            欢迎来到管理后台
          </h1>
          <div className="text-yellow-700 font-medium select-none">管理员</div>
        </header>

        {/* 内容区域 */}
        <section className="flex-grow p-12">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-10">
            {[1, 2, 3, 4, 5, 6].map((idx) => (
              <div
                key={idx}
                className="relative rounded-xl bg-gradient-to-br from-yellow-50 to-yellow-100 shadow-lg p-8 flex flex-col justify-between cursor-default select-none"
                style={{
                  boxShadow:
                    "inset 0 0 20px rgba(250, 204, 21, 0.15), 0 6px 15px rgba(250, 204, 21, 0.3)",
                }}
              >
                <h2 className="text-2xl font-extrabold text-yellow-700 mb-4">
                  模块标题 {idx}
                </h2>
                <p className="text-yellow-900 leading-relaxed tracking-wide">
                  这个卡片展示了模块 {idx} 的简洁内容描述，色彩柔和且具有现代感，配合整体明亮的金黄色调营造温暖而充满活力的氛围。
                </p>
                <div className="absolute -top-6 right-6 text-6xl font-bold text-yellow-300 select-none opacity-30 pointer-events-none">
                  {idx}
                </div>
              </div>
            ))}
          </div>
        </section>
      </main>
    </div>
  );
}