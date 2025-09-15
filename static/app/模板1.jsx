import React from "react";
import "@tailwindcss/browser";

export default function App() {
  return (
    <div className="min-h-screen bg-white flex items-center justify-center p-6">
      {/* 整体：极简竖屏设备，黑色边框 */}
      <div
        className="rounded-3xl overflow-hidden border-2 border-black bg-white shadow-lg"
        style={{
          width: "46vw",
          maxWidth: 420,
          aspectRatio: "9/16",
        }}
        aria-label="简约手机示例"
      >

        <div className="w-full h-full flex flex-col bg-white">
          <div className="px-4 pt-3">
            <div className="flex items-center justify-center">
              <div className="w-20 h-0.5 bg-black rounded-full" />
            </div>
          </div>

          <main className="flex-1 p-5 flex items-center justify-center">
            <div className="w-full h-full rounded-2xl bg-gradient-to-b from-gray-50 to-gray-100 border border-black/10 flex items-center justify-center">
              <div
                className="w-11/12 h-11/12 rounded-2xl bg-transparent flex flex-col items-center justify-center"
                aria-hidden="true"
              >

              </div>
            </div>
          </main>

          <div className="py-3 flex items-center justify-center">
            <div className="w-36 h-0.5 bg-black rounded-full" />
          </div>
        </div>
      </div>
    </div>
  );
}