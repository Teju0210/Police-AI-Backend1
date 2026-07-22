export default function Settings() {
  return (
    <div className="min-h-screen text-white">

      <h1 className="text-4xl font-bold">
        Settings
      </h1>

      <p className="text-slate-400 mt-3">
        Manage account and application settings.
      </p>


      <div className="
        mt-8
        bg-white/5
        backdrop-blur-xl
        border
        border-white/10
        rounded-2xl
        p-8
      ">

        <h2 className="text-2xl font-semibold">
          System Preferences
        </h2>

        <p className="text-slate-400 mt-3">
          Profile, security and dashboard preferences.
        </p>

      </div>

    </div>
  );
}