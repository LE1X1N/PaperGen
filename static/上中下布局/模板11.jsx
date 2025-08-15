import React from "react";
import { Cpu, Activity, Layers, MessageSquare, PhoneCall } from "lucide-react";

export default function App() {
  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-b from-neutral-900 via-slate-900 to-neutral-800 text-gray-300 font-sans">
      {/* 顶部 Header */}
      <header className="bg-neutral-900 backdrop-blur-md bg-opacity-60 shadow-lg py-6 px-8 flex items-center justify-between sticky top-0 z-40 border-b border-slate-700">
        <h1 className="text-3xl font-extrabold tracking-widest text-cyan-400 select-none uppercase drop-shadow-[0_2px_6px_rgba(6,182,212,0.7)]">
          TECH·前端框架
        </h1>
        <nav className="space-x-8 text-cyan-400 font-semibold uppercase text-sm tracking-wide">
          <a
            href="#"
            className="hover:text-cyan-300 transition-colors duration-250"
            aria-label="首页"
          >
            首页
          </a>
          <a
            href="#"
            className="hover:text-cyan-300 transition-colors duration-250"
            aria-label="关于我们"
          >
            关于
          </a>
          <a
            href="#"
            className="hover:text-cyan-300 transition-colors duration-250"
            aria-label="服务"
          >
            服务
          </a>
          <a
            href="#"
            className="hover:text-cyan-300 transition-colors duration-250"
            aria-label="联系"
          >
            联系
          </a>
        </nav>
      </header>

      {/* 中间主要内容区 */}
      <main className="flex-grow px-8 py-16 max-w-7xl mx-auto flex flex-col space-y-20 select-none">
        <section className="bg-gradient-to-tr from-slate-800 to-neutral-900 rounded-3xl shadow-2xl p-12 flex flex-col md:flex-row md:space-x-14 items-center border border-cyan-600/40">
          <img
            src="https://placehold.co/420x320/png?text=Tech+Visual"
            alt="科技视觉"
            className="rounded-2xl shadow-lg mb-10 md:mb-0 md:w-1/2 object-cover border border-cyan-700"
            loading="lazy"
          />
          <div className="md:w-1/2">
            <h2 className="text-4xl font-bold text-cyan-400 mb-5 drop-shadow-lg">
              未来科技驱动设计
            </h2>
            <p className="text-slate-300 leading-relaxed text-lg tracking-wide">
              本框架汇聚前沿技术与未来感设计元素，融合冷光蓝渐变、灵动的微交互与科技图标，
              力求打造极致的用户体验，成就高效且赏心悦目的前端页面。
            </p>
          </div>
        </section>

        <section className="grid grid-cols-1 md:grid-cols-4 gap-12 text-center">
          {[
            {
              title: "高性能",
              desc: "优化渲染与加载，极致响应速度。",
              icon: <Cpu size={48} className="mx-auto mb-4 text-cyan-400" />,
              gradient: "from-cyan-600 to-blue-500",
            },
            {
              title: "实时数据",
              desc: "动态变化，精准反映业务指标。",
              icon: <Activity size={48} className="mx-auto mb-4 text-cyan-400" />,
              gradient: "from-cyan-500 to-teal-400",
            },
            {
              title: "模块化",
              desc: "灵活组合，快速构建复杂界面。",
              icon: <Layers size={48} className="mx-auto mb-4 text-cyan-400" />,
              gradient: "from-indigo-600 to-cyan-500",
            },
            {
              title: "智能交互",
              desc: "自然语义，便捷沟通体验。",
              icon: <MessageSquare size={48} className="mx-auto mb-4 text-cyan-400" />,
              gradient: "from-teal-500 to-cyan-400",
            },
          ].map(({ title, desc, icon, gradient }) => (
            <div
              key={title}
              className={`bg-gradient-to-tr ${gradient} rounded-3xl p-8 shadow-2xl backdrop-blur-sm border border-cyan-500/50 hover:scale-[1.06] transition-transform duration-300 cursor-default select-none`}
            >
              {icon}
              <h3 className="text-2xl font-semibold text-white mb-2">{title}</h3>
              <p className="text-cyan-100 leading-relaxed">{desc}</p>
            </div>
          ))}
        </section>
      </main>

      {/* 底部 Footer */}
      <footer className="bg-neutral-900 backdrop-blur-md bg-opacity-70 border-t border-slate-700 text-cyan-400 py-8 px-8 select-none">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row md:justify-between md:items-center space-y-4 md:space-y-0 text-sm tracking-wide">
          <div className="flex items-center space-x-3">
            <PhoneCall size={20} className="text-cyan-400" />
            <span>技术支持：400-888-8888</span>
          </div>
          <div className="space-x-6 flex justify-center md:justify-end">
            <a
              href="#"
              className="hover:text-cyan-300 focus:text-cyan-300 transition-all"
            >
              隐私政策
            </a>
            <a
              href="#"
              className="hover:text-cyan-300 focus:text-cyan-300 transition-all"
            >
              使用条款
            </a>
            <a
              href="#"
              className="hover:text-cyan-300 focus:text-cyan-300 transition-all"
            >
              联系我们
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}