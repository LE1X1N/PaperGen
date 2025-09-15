import React from "react";
import { Sun, Moon, Bell, UserCircle } from "lucide-react";
import { motion } from "framer-motion";

const mockCardData = [
  {
    id: 1,
    title: "探索新鲜事",
    description: "每日推送，发现精彩内容",
    img: "https://placehold.co/600x320/png?text=%E6%96%B0%E9%97%BB%E6%8E%A8%E9%80%81",
  },
  {
    id: 2,
    title: "我的关注",
    description: "时刻掌握关注动态",
    img: "https://placehold.co/600x320/png?text=%E6%88%91%E7%9A%84%E5%85%B3%E6%B3%A8",
  },
];

export default function App() {
  return (
    <div className="flex flex-col h-screen w-full max-w-sm mx-auto bg-gradient-to-b from-purple-700 via-purple-900 to-black text-white font-sans rounded-md shadow-lg overflow-hidden">
      {/* 顶部导航栏 */}
      <header className="flex items-center justify-between px-5 py-3 bg-purple-950 bg-opacity-70 shadow-lg sticky top-0 z-20">
        <div className="flex items-center space-x-3">
          <Sun className="w-6 h-6 text-yellow-400" />
          <h1 className="text-lg font-bold select-none truncate">精彩小程序</h1>
        </div>
        <button
          type="button"
          aria-label="切换夜间模式"
          className="p-1 rounded-full hover:bg-purple-700 transition"
        >
          <Moon className="w-6 h-6 text-indigo-300" />
        </button>
      </header>

      {/* 主要内容区 */}
      <main className="flex-1 overflow-auto px-4 py-4 space-y-5">
        {/* 搜索框 */}
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="relative"
        >
          <input
            type="search"
            placeholder="搜索新闻、关注..."
            className="w-full rounded-full bg-purple-800 bg-opacity-60 placeholder-purple-300 text-purple-100 text-sm py-2 px-4 pl-10 focus:outline-none focus:ring-2 focus:ring-purple-400 transition"
          />
          <Bell className="absolute top-2.5 left-3 w-5 h-5 text-purple-300 pointer-events-none" />
        </motion.div>

        {/* 卡片组 */}
        <section className="space-y-4">
          {mockCardData.map(({ id, title, description, img }) => (
            <motion.article
              key={id}
              initial={{ scale: 0.95, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ duration: 0.4, delay: id * 0.15 }}
              className="bg-gradient-to-tr from-purple-900 to-purple-800 rounded-2xl shadow-xl overflow-hidden cursor-pointer hover:shadow-2xl hover:scale-[1.03] transition-transform duration-300"
            >
              <img
                src={img}
                alt={title}
                className="w-full h-44 object-cover pointer-events-none"
                loading="lazy"
                draggable={false}
              />
              <div className="p-4">
                <h3 className="text-xl font-extrabold truncate">{title}</h3>
                <p className="mt-1 text-purple-300 text-sm line-clamp-2">{description}</p>
              </div>
            </motion.article>
          ))}
        </section>

        {/* 用户信息卡 */}
        <section className="bg-purple-900 bg-opacity-70 rounded-xl shadow-lg flex items-center gap-4 p-4 cursor-default select-none">
          <UserCircle className="w-14 h-14 text-purple-300 flex-shrink-0" />
          <div className="flex flex-col justify-center">
            <h4 className="text-lg font-bold leading-none truncate">微信小程序用户</h4>
            <p className="text-purple-400 text-xs mt-1 truncate">爱生活 · 爱技术 · 爱探索</p>
          </div>
        </section>
      </main>

      {/* 底部导航 */}
      <nav className="flex justify-around bg-purple-950 bg-opacity-80 py-3 shadow-inner select-none rounded-b-md border-t border-purple-800">
        {[
          { icon: <Sun className="w-6 h-6 text-yellow-400" />, label: "首页" },
          { icon: <Bell className="w-6 h-6 text-purple-300" />, label: "消息" },
          { icon: <UserCircle className="w-6 h-6 text-purple-300" />, label: "我" },
        ].map(({ icon, label }) => (
          <button
            key={label}
            type="button"
            className="flex flex-col items-center justify-center gap-1 text-purple-300 hover:text-yellow-300 transition-colors text-xs font-medium"
          >
            {icon}
            <span className="truncate">{label}</span>
          </button>
        ))}
      </nav>
    </div>
  );
}