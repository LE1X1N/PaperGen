import React, { useState } from 'react';
import { Home, Search, User, Bell, Settings, Heart, Star, MessageCircle } from 'lucide-react';

const App = () => {
  // 保留基础交互状态（固定逻辑，不修改）
  const [activeTab, setActiveTab] = useState('home');

  return (
    <div className="max-w-md mx-auto bg-gray-50 min-h-screen relative shadow-lg">
      {/* 顶部导航栏（标题可动态修改） */}
      <div className="bg-gradient-to-r from-blue-500 to-purple-600 text-white p-4 flex justify-between items-center shadow-md">
        {/* 应用名称占位：可替换为模块名称 */}
        <h2 data-slot="app_title" className="text-xl font-bold">应用名称</h2>
        
        {/* 固定操作按钮（框架不变） */}
        <button className="p-2 rounded-full bg-white bg-opacity-20">
          <Bell className="w-5 h-5" />
        </button>
      </div>

      {/* 主要内容区域（核心动态内容区） */}
      <div className="pb-16 pt-5">
        {/* 功能卡片列表占位：可根据模块功能动态生成 */}
        <div data-slot="function_cards" className="space-y-4 px-2">
          {/* 示例卡片（供模型参考格式，实际生成时替换） */}
          <div 
            className="bg-white rounded-xl shadow-sm overflow-hidden mx-3 transition-transform duration-300 hover:scale-[1.02]"
          >
            <div className="p-5">
              <div className="flex items-center mb-4">
                <div className="w-12 h-12 rounded-lg flex items-center justify-center mr-4" style={{ backgroundColor: '#FF6B6B' }}>
                  <Star className="text-white w-6 h-6" />
                </div>
                <h3 className="text-lg font-semibold">功能名称</h3>
              </div>
              <p className="text-gray-600 text-sm mb-4">功能描述</p>
              <button className="w-full py-2 rounded-lg font-medium transition-colors duration-300" style={{ backgroundColor: '#FF6B6B', color: 'white' }}>
                操作按钮
              </button>
            </div>
          </div>
        </div>

        {/* 统计信息区域占位：可动态替换统计数据 */}
        <div data-slot="statistics" className="bg-white rounded-xl shadow-sm m-4 p-5">
          <h3 className="text-lg font-semibold mb-4">数据统计</h3>
          <div className="grid grid-cols-3 gap-4 text-center">
            {/* 示例统计项（供参考，实际生成时替换） */}
            <div>
              <div className="text-2xl font-bold text-blue-500">统计值1</div>
              <div className="text-gray-500 text-sm">指标名称1</div>
            </div>
          </div>
        </div>
      </div>

      {/* 底部标签栏（导航项可动态修改） */}
      <div className="fixed bottom-0 left-1/2 transform -translate-x-1/2 w-full max-w-md bg-white shadow-lg rounded-t-xl">
        <div data-slot="tab_bar" className="flex justify-around py-3">
          {/* 示例标签项（供参考，实际生成时根据模块页面动态生成） */}
          <button
            className={`flex flex-col items-center py-2 px-3 rounded-lg transition-colors duration-300 ${
              activeTab === 'home' ? 'text-blue-500' : 'text-gray-400'
            }`}
            onClick={() => setActiveTab('home')}
          >
            <Home className={`w-5 h-5 ${activeTab === 'home' ? 'text-blue-500' : 'text-gray-400'}`} />
            <span className="text-xs mt-1">首页</span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default App;