import React from "react";
import { Home, User, MessageCircle, Settings } from "lucide-react";
import { motion } from "framer-motion";

const navItems = [
  { id: "home", label: "首页", icon: <Home className="w-5 h-5" /> },
  { id: "messages", label: "消息", icon: <MessageCircle className="w-5 h-5" /> },
  { id: "profile", label: "我", icon: <User className="w-5 h-5" /> },
  { id: "settings", label: "设置", icon: <Settings className="w-5 h-5" /> },
];

const mockContent = {
  home: [
    {
      id: 1,
      title: "每日推荐",
      description: "精选内容，助力高效生活",
      img: "https://placehold.co/600x300/png?text=%E6%AF%8F%E6%97%A5%E6%8E%A8%E8%8D%90",
    },
    {
      id: 2,
      title: "最新活动",
      description: "限时福利，不容错过",
      img: "https://placehold.co/600x300/png?text=%E6%9C%80%E6%96%B0%E6%B4%BB%E5%8A%A8",
    },
  ],
  messages: [
    {
      id: 1,
      user: "小明",
      message: "今天天气真好，一起去打球吧！",
      avatar: "https://placehold.co/80x80/png?text=%E5%B0%8F%E6%98%8E",
    },
    {
      id: 2,
      user: "小红",
      message: "会议时间改到下午3点了。",
      avatar: "https://placehold.co/80x80/png?text=%E5%B0%8F%E7%BA%A2",
    },
  ],
  profile: {
    avatar: "https://placehold.co/100x100/png?text=%E7%94%A8%E6%88%B7",
    nickname: "微信用户",
    points: 1200,
    description: "热爱生活，热爱技术",
  },
  settings: [
    { id: 1, label: "账号与安全" },
    { id: 2, label: "新消息通知" },
    { id: 3, label: "隐私设置" },
    { id: 4, label: "关于我们" },
  ],
};

export default function App() {
  const [activeTab, setActiveTab] = React.useState("home");

  return (
    <div className="flex flex-col h-screen max-w-sm w-full mx-auto bg-gray-50 font-sans text-gray-800 border border-gray-300 rounded-lg shadow-md">
      {/* 顶部导航 */}
      <header className="flex items-center justify-center h-14 bg-white border-b border-gray-300 text-gray-900 font-semibold text-lg rounded-t-lg select-none shadow-sm">
        微信小程序简约模板
      </header>

      {/* 内容区 */}
      <main className="flex-1 px-4 py-3 overflow-auto scrollbar-thin scrollbar-thumb-gray-400 scrollbar-track-gray-100">
        {/* 首页 */}
        {activeTab === "home" && (
          <section>
            <h2 className="text-2xl font-semibold mb-4 text-gray-900 select-none">首页精选</h2>
            <div className="space-y-5">
              {mockContent.home.map((item) => (
                <motion.div
                  key={item.id}
                  className="bg-white rounded-lg shadow-sm overflow-hidden cursor-pointer hover:shadow-md transition-shadow duration-200"
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.97 }}
                >
                  <img
                    src={item.img}
                    alt={item.title}
                    className="w-full h-36 object-cover rounded-t-lg select-none"
                    loading="lazy"
                    draggable={false}
                  />
                  <div className="p-4">
                    <h3 className="text-lg font-semibold mb-1 truncate">{item.title}</h3>
                    <p className="text-gray-600 text-sm truncate">{item.description}</p>
                  </div>
                </motion.div>
              ))}
            </div>
          </section>
        )}

        {/* 消息 */}
        {activeTab === "messages" && (
          <section>
            <h2 className="text-2xl font-semibold mb-4 text-gray-900 select-none">消息列表</h2>
            <ul className="space-y-3">
              {mockContent.messages.map(({ id, user, message, avatar }) => (
                <motion.li
                  key={id}
                  className="flex items-center bg-white rounded-lg shadow px-4 py-3 cursor-pointer hover:bg-gray-100 transition-colors duration-200"
                  whileHover={{ x: 4 }}
                  whileTap={{ scale: 0.96 }}
                >
                  <img
                    src={avatar}
                    alt={user}
                    className="w-11 h-11 rounded-full mr-4 select-none"
                    loading="lazy"
                    draggable={false}
                  />
                  <div className="flex-1 min-w-0">
                    <p className="font-medium text-gray-900 truncate">{user}</p>
                    <p className="text-gray-700 text-sm truncate">{message}</p>
                  </div>
                </motion.li>
              ))}
            </ul>
          </section>
        )}

        {/* 我 */}
        {activeTab === "profile" && (
          <section className="bg-white rounded-lg shadow p-6 text-center select-none">
            <motion.img
              src={mockContent.profile.avatar}
              alt="头像"
              className="w-24 h-24 rounded-full mx-auto mb-4 border border-gray-300"
              loading="lazy"
              draggable={false}
              whileHover={{ scale: 1.05 }}
              transition={{ type: "spring", stiffness: 250 }}
            />
            <h2 className="text-2xl font-semibold mb-2 truncate">{mockContent.profile.nickname}</h2>
            <p className="text-gray-800 font-medium text-lg mb-1">积分: {mockContent.profile.points}</p>
            <p className="text-gray-600 text-base">{mockContent.profile.description}</p>
          </section>
        )}

        {/* 设置 */}
        {activeTab === "settings" && (
          <section>
            <h2 className="text-2xl font-semibold mb-4 text-gray-900 select-none">设置</h2>
            <ul className="bg-white rounded-lg shadow divide-y divide-gray-200">
              {mockContent.settings.map(({ id, label }) => (
                <motion.li
                  key={id}
                  className="px-6 py-4 cursor-pointer flex justify-between items-center hover:bg-gray-100 transition-colors rounded-lg mx-2 my-1"
                  whileTap={{ scale: 0.95 }}
                  whileHover={{ scale: 1.01 }}
                >
                  <span className="text-gray-900 font-medium truncate">{label}</span>
                  <svg
                    className="w-6 h-6 text-gray-500 flex-shrink-0"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    viewBox="0 0 24 24"
                    aria-hidden="true"
                  >
                    <path d="M9 18l6-6-6-6" />
                  </svg>
                </motion.li>
              ))}
            </ul>
          </section>
        )}
      </main>

      {/* 底部导航 */}
      <nav className="flex justify-around bg-white border-t border-gray-300 h-16 items-center shadow-inner rounded-b-lg select-none">
        {navItems.map(({ id, label, icon }) => {
          const active = activeTab === id;
          return (
            <button
              key={id}
              onClick={() => setActiveTab(id)}
              className={`flex flex-col items-center justify-center max-w-[64px] truncate focus:outline-none transition-colors duration-200 ${
                active ? "text-gray-900" : "text-gray-500 hover:text-gray-700"
              }`}
              aria-label={label}
              title={label}
              type="button"
            >
              {React.cloneElement(icon, {
                strokeWidth: active ? 2.2 : 1.5,
                className: `w-6 h-6 mb-0.5`,
              })}
              <span className="text-[11px] font-normal leading-none truncate w-full">{label}</span>
            </button>
          );
        })}
      </nav>
    </div>
  );
}