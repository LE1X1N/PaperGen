import React from "react";
import { Laptop, Bell, User } from "lucide-react";

const navItems = ["首页", "产品", "关于我们"];
const sidebarItems = [
  {
    key: "sub1",
    icon: <User size={18} className="text-gray-500" />,
    label: "用户管理",
    children: ["用户列表", "权限设置", "角色管理", "操作日志"],
  },
  {
    key: "sub2",
    icon: <Laptop size={18} className="text-gray-500" />,
    label: "设备监控",
    children: ["设备状态", "告警信息", "设备配置", "统计报表"],
  },
  {
    key: "sub3",
    icon: <Bell size={18} className="text-gray-500" />,
    label: "系统通知",
    children: ["通知列表", "消息设置", "更新日志", "帮助中心"],
  },
];

export default function App() {
  const [selectNav, setSelectNav] = React.useState(0);
  const [selectSubMenu, setSelectSubMenu] = React.useState("sub1");
  const [selectSubItem, setSelectSubItem] = React.useState(0);

  return (
    <div className="flex flex-col min-h-screen bg-gradient-to-b from-white via-gray-50 to-gray-100 text-gray-800">
      {/* 顶部导航 */}
      <header className="flex items-center justify-between h-14 px-6 bg-white border-b border-gray-200 shadow-sm sticky top-0 z-30">
        <div className="text-2xl font-extrabold text-indigo-600 select-none tracking-wide">
          Logo
        </div>
        <nav className="flex space-x-8 text-gray-600 text-lg font-medium select-none">
          {navItems.map((item, idx) => (
            <button
              key={item}
              onClick={() => setSelectNav(idx)}
              className={`relative px-1 transition-colors duration-300 hover:text-indigo-600 focus:outline-none focus-visible:text-indigo-600 ${
                selectNav === idx ? "text-indigo-600" : ""
              }`}
              aria-current={selectNav === idx ? "page" : undefined}
            >
              {item}
              {selectNav === idx && (
                <span className="absolute left-0 -bottom-1 w-full h-[2px] bg-indigo-600 rounded-full"></span>
              )}
            </button>
          ))}
        </nav>
      </header>

      {/* 主体部分：侧边栏 + 内容 */}
      <div className="flex flex-1 max-w-[1280px] mx-auto mt-6 mb-12 px-4 sm:px-6 lg:px-8 w-full min-h-[calc(100vh-3.5rem-6rem)]">
        {/* 侧边栏 */}
        <aside className="w-60 bg-white rounded-lg shadow border border-gray-200 sticky top-20 h-[calc(100vh-5.5rem)] overflow-auto py-6">
          {sidebarItems.map(({ key, icon, label, children }) => (
            <div key={key} className="mb-8 last:mb-0">
              <div className="flex items-center px-6 mb-3 text-gray-700 font-semibold text-base select-none tracking-wide">
                <span className="mr-3">{icon}</span>
                {label}
              </div>
              <ul role="list" className="space-y-1">
                {children.map((child, i) => {
                  const isSelected = selectSubMenu === key && selectSubItem === i;
                  return (
                    <li key={child} className="list-none">
                      <button
                        onClick={() => {
                          setSelectSubMenu(key);
                          setSelectSubItem(i);
                        }}
                        className={`flex items-center w-full text-gray-600 hover:text-indigo-600 text-sm rounded-md py-2 px-6 transition-colors duration-200 focus:outline-none focus-visible:bg-indigo-50 focus-visible:text-indigo-700 ${
                          isSelected ? "bg-indigo-50 text-indigo-700 font-semibold" : ""
                        }`}
                        aria-current={isSelected ? "true" : undefined}
                      >
                        {child}
                      </button>
                    </li>
                  );
                })}
              </ul>
            </div>
          ))}
        </aside>

        {/* 内容区 */}
        <main className="flex-1 bg-white rounded-lg shadow border border-gray-200 p-8 min-h-[520px] select-text">
          <h1 className="text-3xl font-extrabold text-gray-900 mb-8 tracking-tight">
            {sidebarItems.find((item) => item.key === selectSubMenu)?.children[selectSubItem] ||
              "欢迎"}
          </h1>
          <section className="text-gray-700 leading-relaxed space-y-5 text-base max-w-3xl">
            <p>
              这是一个简约大方的【顶部-侧边布局】页面示例。页面顶部包含清晰易用的导航栏，侧边栏分组明细，内容区域保持宽敞，方便展示主要信息与功能。
            </p>
            <p>
              页面整体配色明快，采用了舒适的灰白和薰衣草蓝色调，结合适度圆角和阴影，提升质感与层次感。响应式设计保证了在不同屏幕宽度下的良好展示。
            </p>
            <p>
              你可以根据需求替换导航名称、侧边菜单项和内容区域，搭建个性化展示类网站，例如管理后台、信息门户或内容发布平台。
            </p>
          </section>
        </main>
      </div>

      {/* 底部 */}
      <footer className="py-4 text-center border-t border-gray-200 bg-white text-sm text-gray-600 select-none">
        版权所有 © 2024 由优秀团队打造
      </footer>
    </div>
  );
}