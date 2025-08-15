import React, { useState } from "react";
import {
  Home,
  Monitor,
  User,
  Users,
  FileText,
} from "lucide-react";

const menuData = [
  {
    key: "1",
    label: "功能1",
    icon: <Home className="w-5 h-5" />,
  },
  {
    key: "2",
    label: "功能2",
    icon: <Monitor className="w-5 h-5" />,
  },
  {
    key: "sub1",
    label: "用户",
    icon: <User className="w-5 h-5" />,
    children: [
      { key: "3", label: "Tom" },
      { key: "4", label: "Bill" },
      { key: "5", label: "Alex" },
    ],
  },
  {
    key: "sub2",
    label: "团队",
    icon: <Users className="w-5 h-5" />,
    children: [
      { key: "6", label: "团队1" },
      { key: "7", label: "团队2" },
    ],
  },
  {
    key: "9",
    label: "文件",
    icon: <FileText className="w-5 h-5" />,
  },
];

function MenuItem({ item, level = 0, activeKey, onSelect }) {
  const [open, setOpen] = useState(false);

  const hasChildren = item.children && item.children.length > 0;
  const isActive = activeKey === item.key;

  return (
    <div className={`${level === 0 ? "" : "pl-6"}`}>
      <button
        type="button"
        onClick={() => {
          if (hasChildren) {
            setOpen(!open);
          } else {
            onSelect(item.key);
          }
        }}
        className={`flex items-center w-full py-2 px-4 rounded-lg transition-colors duration-200
          ${
            isActive
              ? "bg-pink-600 text-white shadow-lg"
              : "text-purple-900 hover:bg-pink-400/70 hover:text-white"
          }
        `}
        aria-expanded={hasChildren ? open : undefined}
        aria-haspopup={hasChildren ? "true" : undefined}
      >
        {item.icon && <span className="mr-3 flex-shrink-0">{item.icon}</span>}
        <span className="flex-1 text-left font-medium">{item.label}</span>
        {hasChildren && (
          <svg
            className={`w-4 h-4 ml-auto transition-transform duration-300 ${
              open ? "rotate-90" : ""
            }`}
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
            aria-hidden="true"
          >
            <path strokeLinecap="round" strokeLinejoin="round" d="M9 5l7 7-7 7"></path>
          </svg>
        )}
      </button>
      {hasChildren && open && (
        <div className="mt-1">
          {item.children.map((child) => (
            <MenuItem
              key={child.key}
              item={child}
              level={level + 1}
              activeKey={activeKey}
              onSelect={onSelect}
            />
          ))}
        </div>
      )}
    </div>
  );
}

export default function App() {
  const [collapsed, setCollapsed] = useState(false);
  const [selectedKey, setSelectedKey] = useState("1");

  return (
    <div className="flex min-h-screen bg-gradient-to-tr from-pink-200 via-purple-200 to-yellow-200 font-sans text-purple-900">
      {/* 侧边栏 */}
      <aside
        className={`flex flex-col bg-gradient-to-b from-purple-300 via-pink-300 to-yellow-300 shadow-xl select-none transition-width duration-300 ${
          collapsed ? "w-16" : "w-64"
        }`}
      >
        <div
          className={`flex items-center justify-center h-16 font-extrabold text-white tracking-widest drop-shadow-lg px-4 border-b border-purple-400 ${
            collapsed ? "text-2xl" : "text-3xl"
          }`}
        >
          {!collapsed ? "梦幻侧栏" : "梦"}
        </div>
        <nav className="flex-1 overflow-y-auto px-1 mt-4">
          {menuData.map((item) => (
            <MenuItem
              key={item.key}
              item={item}
              activeKey={selectedKey}
              onSelect={(key) => setSelectedKey(key)}
            />
          ))}
        </nav>
        <button
          type="button"
          aria-label={collapsed ? "展开侧边栏" : "收起侧边栏"}
          onClick={() => setCollapsed(!collapsed)}
          className="h-12 flex items-center justify-center text-purple-900 hover:text-white hover:bg-purple-600 transition-colors focus:outline-none"
        >
          <svg
            className={`w-6 h-6 transform transition-transform duration-300 ${
              collapsed ? "rotate-180" : "rotate-0"
            }`}
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path strokeLinecap="round" strokeLinejoin="round" d="M15 19l-7-7 7-7"></path>
          </svg>
        </button>
        <div className="text-center text-purple-800 text-xs py-3 select-text border-t border-purple-400">
          © 2024 梦幻模板
        </div>
      </aside>
      {/* 主内容区 */}
      <main className="flex-1 p-10 max-w-screen-lg mx-auto">
        <h1 className="text-4xl font-extrabold mb-6 text-purple-900 drop-shadow-md">
          欢迎体验梦幻温暖侧边布局模版
        </h1>
        <p className="text-lg text-purple-700 leading-relaxed max-w-3xl">
          这是一个现代且统一风格的侧边栏布局示例，采用柔和温暖的配色和梦幻渐变。
          侧边栏通过点击可展开层级菜单，方便用户访问不同功能模块。整体设计简洁大方，
          并且有细腻的交互动效提升用户体验。页面内容区域留白充分，易于后续扩展实际业务内容。
        </p>
        <section className="mt-12 p-8 rounded-xl bg-purple-100 bg-opacity-60 shadow-lg border border-purple-200">
          <h2 className="text-2xl font-semibold mb-4 text-purple-900">当前选择</h2>
          <p className="text-purple-800 text-lg min-h-[96px]">
            {(() => {
              function findLabel(data, key) {
                for (const item of data) {
                  if (item.key === key) return item.label;
                  if (item.children) {
                    const found = findLabel(item.children, key);
                    if (found) return found;
                  }
                }
                return null;
              }
              return findLabel(menuData, selectedKey) || "请从左侧菜单选择功能或子功能";
            })()}
          </p>
        </section>
      </main>
    </div>
  );
}