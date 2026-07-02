export default function Header() {
  return (
    <header className="bg-white border-b shadow-sm">
      <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-800">
            SHL AI Agent
          </h1>

          <p className="text-sm text-gray-500">
            AI-powered SHL Assessment Recommendation System
          </p>
        </div>

        <div className="text-sm bg-green-100 text-green-700 px-3 py-1 rounded-full">
          Online
        </div>
      </div>
    </header>
  );
}