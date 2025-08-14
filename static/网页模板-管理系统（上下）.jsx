import React, { useState, useEffect } from 'react';
import { Home, User, Folder, Settings, Bell, Search } from 'lucide-react';

const App = () => {
  // 保留基础交互状态（固定逻辑，不修改）
  const [activeTab, setActiveTab] = useState('home');
  const [currentTime, setCurrentTime] = useState(new Date().toLocaleString('zh-CN'));

  // 更新时间（固定逻辑，不修改）
  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date().toLocaleString('zh-CN'));
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      {/* 顶部功能区（框架固定，内容可替换） */}
      <div className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* 顶部信息栏 */}
          <div className="flex items-center justify-between py-4">
            <div className="flex items-center">
              {/* 系统名称占位：可替换为实际系统名称 */}
              <h1 data-slot="system_name" className="text-2xl font-bold text-gray-900">智能管理系统</h1>
            </div>
            
            <div className="flex items-center space-x-6">
              <div className="flex items-center space-x-4">
                {/* 管理员名称占位：可替换为实际用户名 */}
                <span data-slot="admin_name" className="text-gray-600 text-sm">
                  管理员：admin
                </span>
                {/* 时间显示固定：无需修改 */}
                <span className="text-gray-500 text-sm">
                  {currentTime}
                </span>
              </div>
              
              {/* 通知按钮固定：框架不变 */}
              <button className="p-2 rounded-full hover:bg-gray-100 relative">
                <Bell className="h-5 w-5 text-gray-600" />
                <span className="absolute top-1 right-1 h-2 w-2 bg-red-500 rounded-full"></span>
              </button>
            </div>
          </div>
          
          {/* 功能标签导航（可根据模块页面动态生成） */}
          <div className="border-t border-gray-200">
            <nav data-slot="function_tabs" className="flex space-x-8">
              {/* 示例标签项（供参考格式，实际生成时替换） */}
              <button
                key="home"
                onClick={() => setActiveTab('home')}
                className={`flex items-center px-1 py-4 border-b-2 font-medium text-sm transition-colors duration-200 ${
                  activeTab === 'home'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <Home className={`mr-2 h-5 w-5 ${activeTab === 'home' ? 'text-blue-600' : 'text-gray-500'}`} />
                首页
              </button>
            </nav>
          </div>
        </div>
      </div>

      {/* 下方显示区（核心内容动态替换） */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* 页面内容占位：根据当前激活的标签动态显示对应内容 */}
        <div data-slot="page_content">
          {/* 示例内容（首页）：供参考格式，实际生成时替换 */}
          <div className="space-y-6">
            <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-8">
              <h2 className="text-2xl font-bold text-gray-800 mb-4">系统概览</h2>
              <p className="text-gray-600 leading-relaxed text-lg">
                欢迎使用智能管理系统！这是一个现代化的管理系统，为您提供高效、便捷的操作体验。
                通过上方功能区，您可以快速切换不同的功能模块，管理您的数据和设置。
              </p>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default App;
