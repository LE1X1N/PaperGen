import React, { useState } from 'react';
import { Home, Search, User, Bell, Settings, Heart, Star, MessageCircle } from 'lucide-react';

const App = () => {
  const [activeTab, setActiveTab] = useState('home');

  const tabItems = [
    { key: 'home', icon: Home, label: '首页' },
    { key: 'search', icon: Search, label: '搜索' },
    { key: 'favorites', icon: Heart, label: '收藏' },
    { key: 'messages', icon: MessageCircle, label: '消息' },
    { key: 'profile', icon: User, label: '我的' }
  ];

  const functionItems = [
    { 
      title: '功能1', 
      description: '这是第一个核心功能模块，提供基础服务',
      icon: Star,
      color: '#FF6B6B'
    },
    { 
      title: '功能2', 
      description: '第二个功能模块，扩展更多实用特性',
      icon: Settings,
      color: '#4ECDC4'
    },
    { 
      title: '功能3', 
      description: '第三个功能模块，满足个性化需求',
      icon: Bell,
      color: '#45B7D1'
    }
  ];

  return (
    <div className="max-w-md mx-auto bg-gray-50 min-h-screen relative shadow-lg">
      {/* 顶部导航栏 */}
      <div className="bg-gradient-to-r from-blue-500 to-purple-600 text-white p-4 flex justify-between items-center shadow-md">
        <h2 className="text-xl font-bold">应用名称</h2>
        <button className="p-2 rounded-full bg-white bg-opacity-20">
          <Bell className="w-5 h-5" />
        </button>
      </div>

      {/* 主要内容区域 */}
      <div className="pb-16 pt-5">
        <div className="space-y-4 px-2">
          {functionItems.map((item, index) => (
            <div 
              key={index}
              className="bg-white rounded-xl shadow-sm overflow-hidden mx-3 transition-transform duration-300 hover:scale-[1.02]"
            >
              <div className="p-5">
                <div className="flex items-center mb-4">
                  <div 
                    className="w-12 h-12 rounded-lg flex items-center justify-center mr-4"
                    style={{ backgroundColor: item.color }}
                  >
                    <item.icon className="text-white w-6 h-6" />
                  </div>
                  <h3 className="text-lg font-semibold">{item.title}</h3>
                </div>
                <p className="text-gray-600 text-sm mb-4">{item.description}</p>
                <button 
                  className="w-full py-2 rounded-lg font-medium transition-colors duration-300"
                  style={{ backgroundColor: item.color, color: 'white' }}
                >
                  立即体验
                </button>
              </div>
            </div>
          ))}
        </div>

        {/* 统计信息区域 */}
        <div className="bg-white rounded-xl shadow-sm m-4 p-5">
          <h3 className="text-lg font-semibold mb-4">数据统计</h3>
          <div className="grid grid-cols-3 gap-4 text-center">
            <div>
              <div className="text-2xl font-bold text-blue-500">1,234</div>
              <div className="text-gray-500 text-sm">用户数</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-teal-500">567</div>
              <div className="text-gray-500 text-sm">活跃度</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-cyan-500">89%</div>
              <div className="text-gray-500 text-sm">满意度</div>
            </div>
          </div>
        </div>
      </div>

      {/* 底部标签栏 */}
      <div className="fixed bottom-0 left-1/2 transform -translate-x-1/2 w-full max-w-md bg-white shadow-lg rounded-t-xl">
        <div className="flex justify-around py-3">
          {tabItems.map((item) => (
            <button
              key={item.key}
              className={`flex flex-col items-center py-2 px-3 rounded-lg transition-colors duration-300 ${
                activeTab === item.key 
                  ? 'text-blue-500' 
                  : 'text-gray-400'
              }`}
              onClick={() => setActiveTab(item.key)}
            >
              <item.icon 
                className={`w-5 h-5 ${
                  activeTab === item.key ? 'text-blue-500' : 'text-gray-400'
                }`} 
              />
              <span className="text-xs mt-1">{item.label}</span>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default App;