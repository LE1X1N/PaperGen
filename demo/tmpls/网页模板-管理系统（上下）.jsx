import React, { useState, useEffect } from 'react';
import { Home, User, Folder, Settings, Bell, Search } from 'lucide-react';

const App = () => {
  const [activeTab, setActiveTab] = useState('home');
  const [currentTime, setCurrentTime] = useState(new Date().toLocaleString('zh-CN'));

  // 更新时间
  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date().toLocaleString('zh-CN'));
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  // 系统信息配置
  const systemConfig = {
    name: '智能管理系统',
    adminName: 'admin'
  };

  // 功能标签项
  const tabItems = [
    { id: 'home', label: '首页', icon: Home },
    { id: 'func1', label: '功能1', icon: User },
    { id: 'func1', label: '功能2', icon: Folder },
    { id: 'func1', label: '功能3', icon: Settings }
  ];

  // 渲染页面内容
  const renderPageContent = () => {
    switch (activeTab) {
      case 'home':
        return (
          <div className="space-y-6">
            
            <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-8">
              <h2 className="text-2xl font-bold text-gray-800 mb-4">系统概览</h2>
              <p className="text-gray-600 leading-relaxed text-lg">
                欢迎使用{systemConfig.name}！这是一个现代化的管理系统，为您提供高效、便捷的操作体验。
                通过上方功能区，您可以快速切换不同的功能模块，管理您的数据和设置。
              </p>
            </div>
          </div>
        );
      
      
      default:
        return (
          <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">页面未找到</h2>
            <p className="text-gray-600">您访问的页面不存在，请检查导航链接。</p>
          </div>
        );
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      {/* 顶部功能区 */}
      <div className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* 顶部信息栏 */}
          <div className="flex items-center justify-between py-4">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-gray-900">{systemConfig.name}</h1>
            </div>
            
            <div className="flex items-center space-x-6">
              <div className="flex items-center space-x-4">
                <span className="text-gray-600 text-sm">
                  管理员：{systemConfig.adminName}
                </span>
                <span className="text-gray-500 text-sm">
                  {currentTime}
                </span>
              </div>
              
              <button className="p-2 rounded-full hover:bg-gray-100 relative">
                <Bell className="h-5 w-5 text-gray-600" />
                <span className="absolute top-1 right-1 h-2 w-2 bg-red-500 rounded-full"></span>
              </button>
            </div>
          </div>
          
          {/* 功能标签导航 */}
          <div className="border-t border-gray-200">
            <nav className="flex space-x-8">
              {tabItems.map((tab) => {
                const IconComponent = tab.icon;
                const isActive = activeTab === tab.id;
                
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`flex items-center px-1 py-4 border-b-2 font-medium text-sm transition-colors duration-200 ${
                      isActive
                        ? 'border-blue-500 text-blue-600'
                        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                    }`}
                  >
                    <IconComponent className={`mr-2 h-5 w-5 ${isActive ? 'text-blue-600' : 'text-gray-500'}`} />
                    {tab.label}
                  </button>
                );
              })}
            </nav>
          </div>
        </div>
      </div>

      {/* 下方显示区 */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {renderPageContent()}
      </main>
    </div>
  );
};

export default App;