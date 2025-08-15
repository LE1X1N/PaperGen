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
    <div className="flex flex-col h-screen w-full max-w-sm mx-auto bg-gray-50 text-gray-900 font-sans border border-gray-200 rounded-md shadow-lg">
      {/* 顶部导航栏 */}
      <header className="flex items-center justify-center relative bg-gradient-to-r from-green-400 to-green-600 text-white h-14 shadow-md sticky top-0 z-10 rounded-t-md">
        <h1 className="text-lg font-semibold select-none truncate px-4">
          微信小程序通用模板
        </h1>
      </header>

      {/* 主体内容区域 */}
      <main className="flex-1 overflow-auto px-3 py-2">
        {/* 内容根据activeTab切换 */}
        {activeTab === "home" && (
          <section>
            <h2 className="text-xl font-bold mb-3 px-1">首页精选</h2>
            <div className="space-y-4">
              {mockContent.home.map((item) => (
                <motion.div
                  key={item.id}
                  className="bg-white rounded-lg shadow-md overflow-hidden cursor-pointer hover:shadow-lg transition-shadow"
                  whileHover={{ scale: 1.03 }}
                >
                  <img
                    src={item.img}
                    alt={item.title}
                    className="w-full object-cover h-36 rounded-t-lg"
                    loading="lazy"
                    draggable={false}
                  />
                  <div className="p-3">
                    <h3 className="text-lg font-semibold mb-1 truncate">{item.title}</h3>
                    <p className="text-gray-600 text-sm truncate">{item.description}</p>
                  </div>
                </motion.div>
              ))}
            </div>
          </section>
        )}

        {activeTab === "messages" && (
          <section>
            <h2 className="text-xl font-bold mb-3 px-1">消息列表</h2>
            <ul className="space-y-2">
              {mockContent.messages.map(({ id, user, message, avatar }) => (
                <motion.li
                  key={id}
                  className="bg-white rounded-lg shadow flex items-center px-3 py-2 cursor-pointer hover:bg-green-50 transition-colors"
                  whileHover={{ x: 5 }}
                >
                  <img
                    src={avatar}
                    alt={user}
                    className="w-10 h-10 rounded-full mr-3 flex-shrink-0"
                    loading="lazy"
                    draggable={false}
                  />
                  <div className="flex-1 min-w-0">
                    <p className="font-semibold text-gray-900 truncate">{user}</p>
                    <p className="text-gray-700 text-sm truncate">{message}</p>
                  </div>
                </motion.li>
              ))}
            </ul>
          </section>
        )}

        {activeTab === "profile" && (
          <section className="max-w-full mx-auto bg-white rounded-lg shadow-md p-5 text-center">
            <img
              src={mockContent.profile.avatar}
              alt="头像"
              className="w-20 h-20 rounded-full mx-auto mb-3"
              loading="lazy"
              draggable={false}
            />
            <h2 className="text-2xl font-semibold mb-1 truncate">
              {mockContent.profile.nickname}
            </h2>
            <p className="text-green-600 font-bold text-lg mb-1">
              积分: {mockContent.profile.points}
            </p>
            <p className="text-gray-600 text-sm truncate">{mockContent.profile.description}</p>
          </section>
        )}

        {activeTab === "settings" && (
          <section className="max-w-full mx-auto px-1">
            <h2 className="text-xl font-bold mb-3">设置</h2>
            <ul className="bg-white rounded-lg shadow divide-y divide-gray-200">
              {mockContent.settings.map(({ id, label }) => (
                <motion.li
                  key={id}
                  className="px-5 py-3 cursor-pointer hover:bg-green-50 flex justify-between items-center"
                  whileTap={{ scale: 0.95 }}
                >
                  <span className="truncate">{label}</span>
                  <svg
                    className="w-5 h-5 text-green-600 flex-shrink-0"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    viewBox="0 0 24 24"
                    aria-hidden="true"
                  >
                    <path d="M9 18l6-6-6-6"></path>
                  </svg>
                </motion.li>
              ))}
            </ul>
          </section>
        )}
      </main>

      {/* 底部导航栏 */}
      <nav className="flex justify-around bg-white border-t border-gray-200 h-14 items-center shadow-inner select-none rounded-b-md">
        {navItems.map(({ id, label, icon }) => {
          const active = activeTab === id;
          return (
            <button
              key={id}
              onClick={() => setActiveTab(id)}
              className={`flex flex-col items-center justify-center focus:outline-none transition-colors max-w-[64px] truncate ${
                active ? "text-green-600" : "text-gray-500 hover:text-green-500"
              }`}
              aria-label={label}
              title={label}
              type="button"
            >
              {React.cloneElement(icon, {
                strokeWidth: active ? 2.5 : 1.5,
                className: `w-6 h-6 mb-0.5`,
              })}
              <span className="text-[10px] leading-none truncate w-full">{label}</span>
            </button>
          );
        })}
      </nav>
    </div>
  );
}