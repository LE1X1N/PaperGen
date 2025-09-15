import React from "react";
import { Laptop, Bell, User } from "lucide-react";

const navItems = ["1", "2", "3"].map((key) => ({
  key,
  label: `nav ${key}`,
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
        label: `选项${subKey}`,
      };
    }),
  };
});

export default function App() {
  const [selectedNavKey, setSelectedNavKey] = React.useState("2");
  const [selectedSideKey, setSelectedSideKey] = React.useState("1");
  const [openSubKeys, setOpenSubKeys] = React.useState(["sub1"]);

  return (
    <div className="flex flex-col min-h-screen">
      {/* Header */}
      <header className="bg-gray-900 text-white flex items-center px-6 h-14">
        <div className="text-lg font-bold mr-8 select-none">Logo</div>
        <nav className="flex space-x-6 flex-1 min-w-0">
          {navItems.map(({ key, label }) => (
            <button
              key={key}
              onClick={() => setSelectedNavKey(key)}
              className={`whitespace-nowrap px-3 py-1 rounded-md transition-colors duration-200 ${
                selectedNavKey === key
                  ? "bg-gray-700"
                  : "hover:bg-gray-700/50"
              }`}
            >
              {label}
            </button>
          ))}
        </nav>
      </header>

      {/* Main Layout */}
      <div className="flex flex-1 bg-gray-100">
        {/* Sidebar */}
        <aside className="w-48 bg-white border-r border-gray-300 overflow-y-auto">
          {sideItems.map(({ key, icon, label, children }) => (
            <div key={key} className="border-b border-gray-200">
              <button
                onClick={() => {
                  if (openSubKeys.includes(key)) {
                    setOpenSubKeys((keys) =>
                      keys.filter((k) => k !== key)
                    );
                  } else {
                    setOpenSubKeys((keys) => [...keys, key]);
                  }
                }}
                className="flex items-center gap-2 w-full px-4 py-2 text-gray-700 hover:bg-gray-200 transition-colors"
              >
                <span>{icon}</span>
                <span className="flex-1 text-left font-medium">{label}</span>
                <svg
                  className={`transition-transform duration-300 ${
                    openSubKeys.includes(key) ? "rotate-90" : ""
                  }`}
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  viewBox="0 0 24 24"
                  width="16"
                  height="16"
                  aria-hidden="true"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M9 5l7 7-7 7"
                  />
                </svg>
              </button>
              {openSubKeys.includes(key) && (
                <div className="pl-10">
                  {children.map(({ key: childKey, label: childLabel }) => (
                    <button
                      key={childKey}
                      onClick={() => setSelectedSideKey(childKey)}
                      className={`block w-full text-left px-3 py-1 rounded-md mb-1 text-gray-600 transition-colors duration-200 ${
                        selectedSideKey === childKey
                          ? "bg-gray-300 font-semibold"
                          : "hover:bg-gray-200"
                      }`}
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
        <main className="flex-1 p-6">
          {/* Breadcrumb */}
          <nav className="text-sm text-gray-600 mb-4 select-none" aria-label="Breadcrumb">
            <ol className="list-reset flex space-x-2">
              <li>首页</li>
              <li>/</li>
              <li>列表</li>
              <li>/</li>
              <li>应用</li>
            </ol>
          </nav>

          {/* Content Card */}
          <section className="bg-white rounded-lg shadow-md p-6 min-h-[280px]">
            <h2 className="text-xl font-semibold mb-4">内容区</h2>
            <p className="text-gray-700">这里是页面的主要内容区域。</p>
          </section>
        </main>
      </div>
    </div>
  );
}