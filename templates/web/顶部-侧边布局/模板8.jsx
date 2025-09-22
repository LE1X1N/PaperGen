import React from "react";
import { Laptop, Bell, User } from "lucide-react";

const navItems = ["1", "2", "3"].map((key) => ({
  key,
  label: `导航 ${key}`,
}));

const sideItems = [User, Laptop, Bell].map((Icon, index) => {
  const key = String(index + 1);
  return {
    key: `sub${key}`,
    icon: <Icon size={16} />,
    label: `子导航 ${key}`,
    children: Array.from({ length: 4 }).map((_, j) => {
      const subKey = index * 4 + j + 1;
      return {
        key: String(subKey),
        label: `选项 ${subKey}`,
      };
    }),
  };
});

export default function App() {
  const [selectedNavKey, setSelectedNavKey] = React.useState("2");
  const [selectedSideKey, setSelectedSideKey] = React.useState("1");
  const [openSubKeys, setOpenSubKeys] = React.useState(["sub1"]);

  return (
    <div className="flex flex-col min-h-screen bg-gradient-to-br from-pink-50 via-purple-50 to-indigo-50">
      {/* Header */}
      <header className="bg-gradient-to-r from-pink-500 to-purple-600 text-white flex items-center px-6 h-16 shadow-lg select-none font-sans">
        <div className="text-2xl font-extrabold mr-10 tracking-widest drop-shadow-md">
          Youthful 前端模板
        </div>
        <nav className="flex space-x-8 flex-1 min-w-0">
          {navItems.map(({ key, label }) => (
            <button
              key={key}
              onClick={() => setSelectedNavKey(key)}
              className={`whitespace-nowrap px-5 py-2 rounded-lg font-semibold transition-colors duration-300 bg-gradient-to-r ${
                selectedNavKey === key
                  ? "from-pink-300 to-purple-300 text-purple-900 shadow-lg"
                  : "text-white hover:from-pink-400 hover:to-purple-700"
              }`}
              aria-current={selectedNavKey === key ? "page" : undefined}
            >
              {label}
            </button>
          ))}
        </nav>
      </header>

      {/* Main Layout */}
      <div className="flex flex-1 bg-gradient-to-tr from-pink-50 via-purple-50 to-indigo-50">
        {/* Sidebar */}
        <aside className="w-56 bg-white border-r border-pink-200 overflow-y-auto shadow-inner">
          {sideItems.map(({ key, icon, label, children }) => (
            <div key={key} className="border-b border-pink-100">
              <button
                onClick={() => {
                  if (openSubKeys.includes(key)) {
                    setOpenSubKeys((keys) => keys.filter((k) => k !== key));
                  } else {
                    setOpenSubKeys((keys) => [...keys, key]);
                  }
                }}
                className="flex items-center gap-3 w-full px-5 py-3 text-purple-800 font-semibold hover:bg-purple-100 transition-colors rounded-md"
                aria-expanded={openSubKeys.includes(key)}
                aria-controls={`${key}-children`}
              >
                <span className="text-pink-500">{icon}</span>
                <span className="flex-1 text-left">{label}</span>
                <svg
                  className={`transform transition-transform duration-300 text-purple-500 ${
                    openSubKeys.includes(key) ? "rotate-90" : ""
                  }`}
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  viewBox="0 0 24 24"
                  width="18"
                  height="18"
                  aria-hidden="true"
                >
                  <path strokeLinecap="round" strokeLinejoin="round" d="M9 5l7 7-7 7" />
                </svg>
              </button>
              {openSubKeys.includes(key) && (
                <div
                  id={`${key}-children`}
                  className="pl-14 bg-purple-50 border-l border-purple-200 select-none rounded-br-lg rounded-bl-lg"
                >
                  {children.map(({ key: childKey, label: childLabel }) => (
                    <button
                      key={childKey}
                      onClick={() => setSelectedSideKey(childKey)}
                      className={`block w-full text-left px-4 py-2 mb-1 rounded-md font-semibold transition-colors duration-200 ${
                        selectedSideKey === childKey
                          ? "bg-pink-200 text-pink-700 shadow-md"
                          : "text-purple-700 hover:bg-purple-200"
                      }`}
                      aria-current={selectedSideKey === childKey ? "page" : undefined}
                    >
                      {childLabel}
                    </button>
                  ))}
                </div>
              )}
            </div>
          ))}
        </aside>

        {/* Content Area */}
        <main className="flex-1 p-10 overflow-auto">
          {/* Breadcrumb */}
          <nav
            className="text-sm text-purple-600 mb-6 select-none font-semibold tracking-wide"
            aria-label="Breadcrumb"
          >
            <ol className="list-reset flex space-x-3">
              <li>首页</li>
              <li>/</li>
              <li>列表</li>
              <li>/</li>
              <li>应用</li>
            </ol>
          </nav>

          {/* Content Card */}
          <section className="bg-white rounded-3xl shadow-2xl p-12 min-h-[320px] max-w-5xl mx-auto border border-pink-300">
            <h2 className="text-4xl font-extrabold mb-6 text-pink-600 tracking-wide">
              内容区域
            </h2>
            <p className="text-purple-700 leading-relaxed text-lg tracking-wide">
              这里是页面的主要内容区域。采用年轻活力的粉紫渐变色调设计，整体风格清新亮眼，富有现代感与吸引力。
            </p>
          </section>
        </main>
      </div>
    </div>
  );
}