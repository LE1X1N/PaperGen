import React, { useState, useRef, useEffect } from "react";
import {
  Home,
  PieChart,
  Users,
  FileText,
  Layout as LayoutIcon,
  Menu as MenuIcon,
} from "lucide-react";

const menuItems = [
  {
    key: "1",
    label: "仪表盘",
    icon: <PieChart className="w-5 h-5" />,
  },
  {
    key: "2",
    label: "项目管理",
    icon: <LayoutIcon className="w-5 h-5" />,
  },
  {
    key: "sub1",
    label: "用户管理",
    icon: <Users className="w-5 h-5" />,
    children: [
      { key: "3", label: "用户列表" },
      { key: "4", label: "权限设置" },
      { key: "5", label: "角色管理" },
    ],
  },
  {
    key: "sub2",
    label: "文件中心",
    icon: <FileText className="w-5 h-5" />,
    children: [
      { key: "6", label: "文件列表" },
      { key: "7", label: "上传文件" },
    ],
  },
  {
    key: "8",
    label: "菜单管理",
    icon: <MenuIcon className="w-5 h-5" />,
  },
];

export default function App() {
  const [collapsed, setCollapsed] = useState(false);
  const [activeKey, setActiveKey] = useState("1");
  const [openSubmenus, setOpenSubmenus] = useState([]);
  const submenuRefs = useRef({});

  // 初始化子菜单高度
  useEffect(() => {
    Object.keys(submenuRefs.current).forEach(key => {
      const ref = submenuRefs.current[key];
      if (ref && openSubmenus.includes(key)) {
        ref.style.height = `${ref.scrollHeight}px`;
      }
    });
  }, [openSubmenus]);

  const toggleCollapse = () => setCollapsed(prev => !prev);

  const onMenuClick = (key, hasChildren) => {
    if (hasChildren) {
      setOpenSubmenus(prev => {
        const isOpen = prev.includes(key);
        // 更新子菜单高度
        const ref = submenuRefs.current[key];
        if (ref) {
          if (isOpen) {
            ref.style.height = "0px";
          } else {
            ref.style.height = `${ref.scrollHeight}px`;
          }
        }
        return isOpen ? prev.filter(k => k !== key) : [...prev, key];
      });
    } else {
      setActiveKey(key);
    }
  };

  // 计算面包屑
  let breadcrumb = ["首页"];
  menuItems.forEach(item => {
    if (item.key === activeKey) {
      breadcrumb = ["首页", item.label];
    } else if (item.children) {
      const child = item.children.find(c => c.key === activeKey);
      if (child) {
        breadcrumb = ["首页", item.label, child.label];
      }
    }
  });

  return (
    <div className="flex min-h-screen bg-gradient-to-br from-cyan-50 to-blue-50">
      {/* 侧边栏 */}
      <aside
        className={`bg-gradient-to-b from-blue-700 to-blue-900 shadow-lg text-white flex flex-col transition-all duration-300 ease-in-out ${
          collapsed ? "w-16" : "w-60"
        }`}
      >
        <div className="flex items-center justify-between px-4 py-4 border-b border-blue-600">
          <h1
            className={`font-bold text-lg whitespace-nowrap truncate transition-opacity duration-300 ${
              collapsed ? "opacity-0 w-0" : "opacity-100"
            }`}
          >
            我的管理系统
          </h1>
          <button
            onClick={toggleCollapse}
            aria-label={collapsed ? "展开菜单" : "收起菜单"}
            className="p-1 rounded hover:bg-blue-600 transition"
          >
            <MenuIcon className="w-5 h-5" />
          </button>
        </div>

        <nav className="flex-1 overflow-y-auto py-4">
          <ul className="flex flex-col gap-1 px-1">
            {menuItems.map(({ key, label, icon, children }) => {
              const isActive =
                activeKey === key ||
                (children && children.some(c => c.key === activeKey));
              const isOpen = openSubmenus.includes(key);

              return (
                <li key={key} className="select-none">
                  <div
                    onClick={() => onMenuClick(key, !!children)}
                    className={`flex items-center cursor-pointer rounded-md px-3 py-2 hover:bg-blue-600 transition-colors gap-3 ${
                      isActive ? "bg-blue-800 font-semibold shadow-md" : ""
                    }`}
                  >
                    <div className="flex-shrink-0">{icon}</div>
                    {!collapsed && (
                      <span className="flex-1 text-sm">{label}</span>
                    )}
                    {!collapsed && children && (
                      <span
                        className={`inline-block transition-transform duration-300 ease-in-out ${
                          isOpen ? "rotate-90" : ""
                        }`}
                      >
                        ▶
                      </span>
                    )}
                  </div>
                  {children && !collapsed && (
                    <ul
                      ref={el => submenuRefs.current[key] = el}
                      className={`pl-10 flex flex-col gap-1 overflow-hidden transition-all duration-300 ease-in-out ${
                        !isOpen ? "h-0 opacity-0" : "opacity-100"
                      }`}
                      style={{ height: isOpen ? 'auto' : '0px' }}
                    >
                      {children.map(({ key: cKey, label: cLabel }) => (
                        <li key={cKey}>
                          <button
                            onClick={() => setActiveKey(cKey)}
                            className={`w-full text-left rounded-md px-3 py-2 text-sm hover:bg-blue-600 transition-colors ${
                              activeKey === cKey
                                ? "bg-blue-700 font-semibold shadow-inner"
                                : ""
                            }`}
                          >
                            {cLabel}
                          </button>
                        </li>
                      ))}
                    </ul>
                  )}
                </li>
              );
            })}
          </ul>
        </nav>

        <div
          className={`text-xs text-blue-300 px-4 py-3 border-t border-blue-600 select-none transition-all duration-300 ${
            collapsed ? "text-center" : ""
          }`}
        >
          {collapsed ? "© 23" : "© 2023 前端设计框架"}
        </div>
      </aside>

      {/* 主体内容 */}
      <main className="flex-1 flex flex-col px-6 py-6">
        {/* 面包屑 */}
        <nav
          aria-label="面包屑"
          className="text-gray-600 text-sm mb-4 select-none"
        >
          {breadcrumb.map((bc, idx) => (
            <span key={bc} className="inline-flex items-center">
              {idx > 0 && (
                <svg
                  className="w-4 h-4 mx-1 text-gray-400"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  viewBox="0 0 24 24"
                  xmlns="http://www.w3.org/2000/svg"
                  aria-hidden="true"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M9 5l7 7-7 7"
                  ></path>
                </svg>
              )}
              <span>{bc}</span>
            </span>
          ))}
        </nav>

        {/* 内容卡片 */}
        <article className="bg-white rounded-lg shadow-md p-6 flex-1 overflow-auto">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">
            {breadcrumb[breadcrumb.length - 1]}
          </h2>
          <p className="text-gray-600 leading-relaxed">
            这是一个通用的前端页面框架示例，基于React和TailwindCSS设计。左侧为可折叠导航栏，右侧为内容展示区域。设计语言统一，颜色搭配协调，支持响应式布局和交互动画。
          </p>
          <p className="mt-4 text-gray-500 text-sm select-none">
            当前页面Key: <code>{activeKey}</code>
          </p>
        </article>

        {/* 页脚 */}
        <footer className="mt-6 text-center text-gray-400 text-xs select-none">
          © 2025 前端设计框架 版权所有
        </footer>
      </main>
    </div>
  );
}
