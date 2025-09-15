import React, { useState, useEffect } from "react";
import { Home, User, Folder, Settings, Bell, LogOut, Menu } from "lucide-react";

const tabs = [
  { id: "home", label: "首页", icon: Home },
  { id: "user", label: "用户管理", icon: User },
  { id: "folder", label: "资料库", icon: Folder },
  { id: "settings", label: "设置", icon: Settings },
];

const App = () => {
  const [activeTab, setActiveTab] = useState("home");
  const [currentTime, setCurrentTime] = useState(
    new Date().toLocaleString("zh-CN")
  );

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date().toLocaleString("zh-CN"));
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  // 当切换标签时添加过渡动画类
  useEffect(() => {
    const content = document.getElementById('tab-content');
    if (content) {
      // 触发重排
      content.classList.remove('animate-fade-in');
      void content.offsetWidth; // 强制重绘
      content.classList.add('animate-fade-in');
    }
  }, [activeTab]);

  const renderContent = () => {
    switch (activeTab) {
      case "home":
        return (
          <div
            id="tab-content"
            className="bg-white rounded-2xl shadow-md border border-gray-200 p-8 transition-all duration-300"
          >
            <h2 className="text-3xl font-extrabold text-gray-900 mb-4">系统概览</h2>
            <p className="text-gray-700 leading-relaxed text-lg">
              欢迎使用现代智能管理系统！界面设计简洁大方，功能丰富且操作便捷，助您高效管理各项任务。
            </p>
          </div>
        );
      case "user":
        return (
          <div
            id="tab-content"
            className="bg-white rounded-2xl shadow-md border border-gray-200 p-8 transition-all duration-300"
          >
            <h2 className="text-3xl font-extrabold text-gray-900 mb-4">用户管理</h2>
            <p className="text-gray-700 leading-relaxed text-lg">
              在这里可以管理系统所有用户，包括添加新用户、编辑用户信息和设置用户权限。
            </p>
          </div>
        );
      case "folder":
        return (
          <div
            id="tab-content"
            className="bg-white rounded-2xl shadow-md border border-gray-200 p-8 transition-all duration-300"
          >
            <h2 className="text-3xl font-extrabold text-gray-900 mb-4">资料库</h2>
            <p className="text-gray-700 leading-relaxed text-lg">
              系统所有文档和资料的存储中心，可以上传、下载和管理各类文件。
            </p>
          </div>
        );
      case "settings":
        return (
          <div
            id="tab-content"
            className="bg-white rounded-2xl shadow-md border border-gray-200 p-8 transition-all duration-300"
          >
            <h2 className="text-3xl font-extrabold text-gray-900 mb-4">系统设置</h2>
            <p className="text-gray-700 leading-relaxed text-lg">
              配置系统参数、安全选项和个性化设置，定制符合您需求的系统环境。
            </p>
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-gray-50 to-gray-100">
      {/* 添加全局样式 */}
      <style jsx global>{`
        .animate-fade-in {
          animation: fadeIn 0.3s ease-out forwards;
        }
        
        @keyframes fadeIn {
          from {
            opacity: 0;
            transform: translateY(12px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
      `}</style>
      
      {/* 上部 Header */}
      <header className="bg-white shadow-md border-b border-gray-300 px-6 h-16 flex items-center justify-between select-none">
        <h1 className="text-2xl font-bold text-gray-900">智能管理系统</h1>
        <div className="flex items-center space-x-8">
          <div className="flex items-center space-x-6 text-gray-700 font-medium text-sm select-text">
            <span>管理员：admin</span>
            <span className="font-normal text-gray-500">{currentTime}</span>
          </div>
          <button
            className="p-2 rounded-full hover:bg-gray-100 relative transition-colors"
            aria-label="通知"
            title="通知"
          >
            <Bell className="w-6 h-6 text-gray-600" />
            <span className="absolute top-2 right-2 h-2.5 w-2.5 bg-red-500 rounded-full animate-pulse"></span>
          </button>
          <button
            className="p-2 rounded-full hover:bg-gray-100 transition-colors text-gray-600"
            title="退出登录"
            aria-label="退出登录"
          >
            <LogOut className="w-6 h-6" />
          </button>
        </div>
      </header>

      {/* 中间功能区 Tabs */}
      <nav className="bg-white shadow-inner border-b border-gray-300 flex justify-center select-none">
        <ul className="flex space-x-12 max-w-4xl w-full px-4 sm:px-6 lg:px-8">
          {tabs.map(({ id, label, icon: Icon }) => (
            <li key={id} className="relative">
              <button
                onClick={() => setActiveTab(id)}
                className={`flex items-center gap-2 py-4 border-b-4 font-semibold text-sm transition-colors duration-300 focus:outline-none
                  ${
                    activeTab === id
                      ? "border-indigo-500 text-indigo-700"
                      : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
                  }`}
                aria-current={activeTab === id ? "page" : undefined}
              >
                <Icon
                  className={`w-5 h-5 ${
                    activeTab === id ? "text-indigo-600" : "text-gray-400"
                  }`}
                />
                {label}
              </button>
            </li>
          ))}
        </ul>
      </nav>

      {/* 下方主内容区 */}
      <main className="flex-1 overflow-y-auto p-8 max-w-7xl mx-auto w-full">
        {renderContent()}
      </main>

      {/* 底部 Footer */}
      <footer className="bg-white border-t border-gray-300 text-gray-500 text-sm text-center py-3 select-text">
        版权所有 &copy; 2024 智能管理系统 - 版权所有
      </footer>
    </div>
  );
};

export default App;
