import React from 'react';
import { Home, User, Folder, Settings, LogOut } from 'lucide-react';
import dayjs from 'dayjs';

const App = () => {
  // 保留时间动态更新逻辑（固定）
  const currentTime = dayjs().format('YYYY-MM-DD HH:mm');

  return (
    <div className="min-h-screen flex bg-slate-50">
      {/* 左侧侧边栏（框架固定，内容可动态替换） */}
      <aside 
        className="bg-slate-800 text-slate-100 w-64 flex flex-col items-center justify-start p-4 shadow-md transition-all duration-300"
      >
        {/* 顶部系统名称（可替换为实际系统名） */}
        <div className="w-full py-4 mb-8 border-b border-slate-700">
          <h1 data-slot="system_name" className="text-xl font-bold text-center tracking-wide text-white">
            XXXX管理系统
          </h1>
        </div>
        
        {/* 导航菜单（可根据模块页面动态生成） */}
        <nav data-slot="sidebar_nav" className="w-full flex-grow">
          <ul className="space-y-1">
            {/* 示例导航项（供参考格式，实际生成时替换） */}
            <li>
              <a href="#" className="flex items-center px-4 py-3 text-sm font-medium rounded-lg bg-indigo-600 text-white">
                <Home className="mr-3 h-5 w-5" />
                功能1
              </a>
            </li>
            <li>
              <a href="#" className="flex items-center px-4 py-3 text-sm font-medium text-slate-200 hover:bg-slate-700 hover:text-white rounded-lg transition-colors duration-200">
                <User className="mr-3 h-5 w-5" />
                功能2
              </a>
            </li>
          </ul>
        </nav>
        
        {/* 底部退出按钮（固定框架，不可修改） */}
        <div className="w-full pt-4 border-t border-slate-700 mt-4">
          <button className="flex items-center justify-center w-full px-4 py-2 text-sm font-medium text-slate-200 hover:bg-slate-700 hover:text-white rounded-lg transition-colors duration-200">
            <LogOut className="mr-2 h-4 w-4" />
            退出登录
          </button>
        </div>
      </aside>


      {/* 右侧主内容区（框架固定，内容可动态替换） */}
      <div className="flex-1 flex flex-col">
        {/* 顶部导航栏 */}
        <header className="bg-white border-b border-slate-200 px-6 py-3 flex items-center justify-between shadow-sm">
          {/* 页面标题（可随当前页面动态变化） */}
          <div data-slot="page_title" className="text-lg font-semibold text-slate-800">
            首页
          </div>
          <div className="flex items-center space-x-6">
            {/* 管理员名称（可动态替换） */}
            <span data-slot="admin_name" className="text-slate-600 text-sm">
              管理员：admin
            </span>
            {/* 时间显示（固定逻辑，不可修改） */}
            <span className="text-slate-500 text-sm">
              {currentTime}
            </span>
          </div>
        </header>

        {/* 页面主体内容（核心动态区域） */}
        <main className="flex-1 p-6 overflow-auto">
          <div data-slot="main_content" className="bg-white rounded-lg shadow-sm border border-slate-100 p-6">
            {/* 示例内容（供参考格式，实际生成时替换） */}
            <h2 className="text-xl font-bold mb-4 text-slate-800">欢迎使用</h2>
            <p className="text-slate-600">
              这里是系统的主页面，您可以通过左侧菜单导航到不同功能模块。
            </p>
          </div>
        </main>
      </div>
    </div>
  );
};

export default App;
