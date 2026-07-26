import React from "react";

export default function Reports() {
  return (
    <div className="min-h-screen p-8 bg-gray-100">
      <h1 className="text-3xl font-bold text-blue-700 mb-6">
        Crime Analytics Reports
      </h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">

        <div className="bg-white rounded-xl shadow-md p-6">
          <h2 className="font-bold text-xl mb-2">District Report</h2>
          <p>District-wise crime analysis and comparison.</p>
        </div>

        <div className="bg-white rounded-xl shadow-md p-6">
          <h2 className="font-bold text-xl mb-2">Crime Trends</h2>
          <p>Monthly and yearly crime trends with charts.</p>
        </div>

        <div className="bg-white rounded-xl shadow-md p-6">
          <h2 className="font-bold text-xl mb-2">Hotspot Analysis</h2>
          <p>Crime hotspot identification using heatmaps.</p>
        </div>

        <div className="bg-white rounded-xl shadow-md p-6">
          <h2 className="font-bold text-xl mb-2">Repeat Offenders</h2>
          <p>Network analysis of repeat offenders.</p>
        </div>

        <div className="bg-white rounded-xl shadow-md p-6">
          <h2 className="font-bold text-xl mb-2">Victim Analysis</h2>
          <p>Age, gender and victim distribution reports.</p>
        </div>

        <div className="bg-white rounded-xl shadow-md p-6">
          <h2 className="font-bold text-xl mb-2">Export Reports</h2>
          <button className="bg-blue-600 text-white px-4 py-2 rounded mt-3">
            Download PDF
          </button>
        </div>

      </div>
    </div>
  );
}
