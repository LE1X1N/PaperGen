import React, { useState } from "react";
import "@tailwindcss/browser";
import {
  Home,
  Settings,
  MessageCircle,
  Camera,
  Calendar,
  Music,
  MapPin,
  ShieldCheck,
  ArrowLeft,
  Search,
  BatteryCharging,
  Wifi,
  Bell,
} from "lucide-react";

export default function App() {

  const [active, setActive] = useState(null);

  return (
    <div className="min-h-screen bg-neutral-100 flex items-center justify-center p-6">
      {/* 手机主体：竖屏 20:9 (使用 width/height = 9/20 来实现高屏幕纵向长条) */}
      <div
        className="rounded-3xl shadow-[0_40px_90px_rgba(2,6,23,0.6)] overflow-hidden transform transition-all hover:scale-[1.01]"
        style={{
          width: "44vw",
          maxWidth: 420,
          aspectRatio: "9/20",
          borderRadius: 28,
        }}
      >
        <div
          className="w-full h-full bg-gradient-to-b from-black/75 to-black/95 flex flex-col"
          role="application"
          aria-label="移动应用模板 20:9"
        >
          {/* 顶部状态栏：更紧凑以适配超高屏幕 */}
          <div className="flex items-center justify-between px-4 pt-3 pb-1">
            <div className="flex items-center gap-3">
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-white/70" />
                <div className="w-2 h-2 rounded-full bg-white/50" />
              </div>
              <div className="text-sm text-white/85 font-medium">上午 9:41</div>
            </div>
            <div className="flex items-center gap-3">
              <Wifi className="text-white/80" size={16} />
              <BatteryCharging className="text-white/80" size={16} />
            </div>
          </div>

          {/* 背景图 + 主内容区：（背景图固定不变） */}
          <div
            className="flex-1 p-4 bg-cover bg-center"
            style={{
              backgroundImage:
                "url('https://images.unsplash.com/photo-1517816743773-6e0fd518b4a6?q=80&w=1200&auto=format&fit=crop&ixlib=rb-4.0.3&s=1c5b1d7a4b2d998b6d3b7b9c5a2f4c6f')",
            }}
          >
            {/* 主内容区 */}
          </div>

          {/* 底部手势条，更靠下以符合长屏比例 */}
          <div className="py-3 flex items-center justify-center">
            <div className="w-36 h-1 rounded-full bg-white/10" />
          </div>
          
        </div>
      </div>
    </div>
  );
}