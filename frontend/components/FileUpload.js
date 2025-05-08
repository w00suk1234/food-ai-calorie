'use client';
import { useState } from 'react';

export default function FileUpload() {
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setImage(file);
    setPreview(URL.createObjectURL(file));
    setResult(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!image) return;

    const formData = new FormData();
    formData.append('image', image);

    setLoading(true);
    try {
      const res = await fetch('http://localhost:8000/api/predict/', {
        method: 'POST',
        body: formData,
      });
      const data = await res.json();
      setResult(data);
    } catch (err) {
      console.error('업로드 실패:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="text-white text-center w-full max-w-xl">
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* 📁 이미지 선택 영역 */}
        <label className="cursor-pointer border-2 border-dashed border-white/50 hover:border-green-400 px-4 py-6 rounded-xl w-full max-w-xs mx-auto block text-center transition-all">
          <div className="text-white text-sm space-y-2">
            <div className="text-2xl">📁</div>
            <div><strong>이미지를 여기에 업로드하거나 클릭하세요</strong></div>
            <div className="text-gray-300 text-xs">(파일 형식: JPG, PNG 등)</div>
          </div>
          <input
            type="file"
            accept="image/*"
            onChange={handleChange}
            className="hidden"
          />
        </label>

        {/* 📦 카드 결과 영역 */}
        <div className="bg-white/10 border border-white/30 p-5 rounded-xl shadow-inner w-full max-w-xs mx-auto">
          {!preview ? (
            <div className="h-[250px] flex items-center justify-center text-gray-300 italic">
              🍱 여기에 음식 이미지를 업로드하면 분석 결과가 나와요
            </div>
          ) : (
            <img
              src={preview}
              alt="업로드 이미지"
              className="rounded-lg shadow w-full h-auto max-h-[400px] object-contain border border-white/50"
            />
          )}

          {result && (
            <div className="mt-4 text-left text-sm space-y-1 bg-black/70 p-4 rounded-lg">
              <p><strong>🍽 음식:</strong> {result.food}</p>
              <p><strong>🔥 칼로리:</strong> {result.calories} kcal</p>
              <p><strong>🥔 탄수화물:</strong> {result.carbs}g</p>
              <p><strong>🍗 단백질:</strong> {result.protein}g</p>
              <p><strong>🧈 지방:</strong> {result.fat}g</p>
              <p className="mt-2 font-medium text-green-300">{result.message}</p>
            </div>
          )}
        </div>

        {/* 🧠 분석 버튼 */}
        <button
          type="submit"
          className="bg-green-600 hover:bg-green-700 px-6 py-2 rounded shadow text-sm"
        >
          {loading ? '분석 중...' : '🧠 AI 분석하기'}
        </button>
      </form>
    </div>
  );
}
