import React from 'react';
import { Home, User, Folder, Settings, LogOut } from 'lucide-react';
import { motion } from 'framer-motion';
import dayjs from 'dayjs';

const App = () => {
  // 系统信息配置
  const systemConfig = {
    name: 'XXXX管理系统',   //根据对应系统变化
    adminName: 'admin',
    currentTime: dayjs().format('YYYY-MM-DD HH:mm')
  };

  return (
    <div className="min-h-screen flex bg-slate-50">
      {/* 左侧侧边栏*/}
      <motion.aside 
        className="bg-slate-800 text-slate-100 w-64 flex flex-col items-center justify-start p-4 shadow-md" 
        initial={{ x: 0 }} 
        animate={{ x: 0 }} 
        transition={{ duration: 0.3 }}
      >
        {/* 顶部系统名称 */}
        <div className="w-full py-4 mb-8 border-b border-slate-700">
          <h1 className="text-xl font-bold text-center tracking-wide text-white">
            {systemConfig.name}
          </h1>
        </div>
        
        {/* 导航菜单*/}
        <nav className="w-full flex-grow">
          <ul className="space-y-1">
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
            <li>
              <a href="#" className="flex items-center px-4 py-3 text-sm font-medium text-slate-200 hover:bg-slate-700 hover:text-white rounded-lg transition-colors duration-200">
                <Folder className="mr-3 h-5 w-5" />
                功能3
              </a>
            </li>
            <li>
              <a href="#" className="flex items-center px-4 py-3 text-sm font-medium text-slate-200 hover:bg-slate-700 hover:text-white rounded-lg transition-colors duration-200">
                <Settings className="mr-3 h-5 w-5" />
                功能4
              </a>
            </li>
          </ul>
        </nav>
        
        {/* 底部退出按钮 */}
        <div className="w-full pt-4 border-t border-slate-700 mt-4">
          <button className="flex items-center justify-center w-full px-4 py-2 text-sm font-medium text-slate-200 hover:bg-slate-700 hover:text-white rounded-lg transition-colors duration-200">
            <LogOut className="mr-2 h-4 w-4" />
            退出登录
          </button>
        </div>
      </motion.aside>


      {/* 右侧主内容区*/}
      <div className="flex-1 flex flex-col">
        {/* 顶部导航栏*/}
        <header className="bg-white border-b border-slate-200 px-6 py-3 flex items-center justify-between shadow-sm">
          <div className="text-lg font-semibold text-slate-800">
            首页
          </div>
          <div className="flex items-center space-x-6">
            <span className="text-slate-600 text-sm">
              管理员：{systemConfig.adminName}
            </span>
            <span className="text-slate-500 text-sm">
              {systemConfig.currentTime}
            </span>
          </div>
        </header>

        {/* 页面主体内容 */}
        <main className="flex-1 p-6 overflow-auto">
          <div className="bg-white rounded-lg shadow-sm border border-slate-100 p-6">
            <h2 className="text-xl font-bold mb-4 text-slate-800">欢迎使用</h2>
            <p className="text-slate-600">
              这里是{systemConfig.name}的主页面，您可以通过左侧菜单导航到不同功能模块。
            </p>
          </div>
        </main>
      </div>
    </div>
  );
};

export default App;