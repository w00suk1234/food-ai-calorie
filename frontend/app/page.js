'use client';
import { useEffect, useState } from 'react';
import FileUpload from '../components/FileUpload';

const images = [
  '/foods/aifood1.png',
  '/foods/aifood2.png',
  '/foods/aifood3.png',
  '/foods/aifood4.png',
];

export default function HomePage() {
  const [index, setIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setIndex((prev) => (prev + 1) % images.length);
    }, 6000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="relative min-h-screen overflow-auto text-white">
      {/* 배경 이미지 */}
      <div
        key={index}
        className="absolute inset-0 z-0 transition-opacity duration-1000 opacity-100"
        style={{
          backgroundImage: `url(${images[index]})`,
          backgroundSize: 'cover',
          backgroundPosition: 'center',
        }}
      />
      {/* 배경 어둡게 + 블러 */}
      <div className="absolute inset-0 z-0 bg-black/20 backdrop-blur-sm" />

      {/* 메인 컨텐츠 */}
      <div className="relative z-10 flex flex-col items-center justify-start px-4 py-20 min-h-screen">
        <h1 className="text-3xl md:text-4xl font-bold text-center mb-6 drop-shadow-xl">
          🍱 AI 음식 칼로리 분석기
        </h1>

        <p className="text-center max-w-md text-gray-100 bg-black/40 border border-white/20 p-4 rounded-xl shadow-lg backdrop-blur-sm text-sm leading-relaxed mb-8">
          업로드한 음식 이미지를 AI가 분석하여<br />
          <span className="text-green-300 font-semibold">칼로리</span>,
          <span className="text-orange-300 font-semibold"> 탄수화물</span>,
          <span className="text-blue-300 font-semibold"> 단백질</span>,
          <span className="text-purple-300 font-semibold"> 지방</span>을 예측합니다.<br />
          <span className="text-pink-400 font-bold underline decoration-pink-300 underline-offset-2">
            다이어트 식단 여부도 함께 확인해보세요!
          </span>
        </p>

        {/* 이미지 업로드 + 결과 */}
        <FileUpload />

        {/* 간단한 푸터 */}
        <div className="mt-12 text-xs text-white/50">
          Made with ❤️ by W00suk | GPT-powered
        </div>
      </div>
    </div>
  );
}
