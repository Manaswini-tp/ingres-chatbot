import React from 'react';

const DataCard = ({ data }) => {
  return (
    <div className="data-card">
      <div className="card-header">
        <h3>{data.district}</h3>
        <span className="state-badge">{data.state}</span>
      </div>
      <div className="card-body">
        {data.rainfall !== null && (
          <div className="data-item">
            <span className="data-label">💧 Rainfall</span>
            <span className="data-value">{data.rainfall} mm</span>
          </div>
        )}
        {data.extraction_stage !== null && (
          <div className="data-item">
            <span className="data-label">📊 Extraction Stage</span>
            <span className={`data-value ${data.extraction_stage > 70 ? 'critical' : ''}`}>
              {data.extraction_stage}%
            </span>
          </div>
        )}
        {data.gw_recharge !== null && (
          <div className="data-item">
            <span className="data-label">♻️ GW Recharge</span>
            <span className="data-value">{data.gw_recharge} ham</span>
          </div>
        )}
        {data.net_availability !== null && (
          <div className="data-item">
            <span className="data-label">💦 Net Availability</span>
            <span className="data-value">{data.net_availability} ham</span>
          </div>
        )}
      </div>
    </div>
  );
};

export default DataCard;
