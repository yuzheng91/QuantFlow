// KLineChart.jsx
import React, { useEffect, useRef, useState } from 'react';
import { createChart } from 'lightweight-charts';
import Papa from 'papaparse';

const KLineChart = ({
  signals = [],
  kline = [],
  symbol,
  startDate,
  endDate,
}) => {
  console.log("🧾 Symbol:", symbol);
  console.log("📆 Date range:", startDate, "to", endDate);

  const chartRef = useRef();

  useEffect(() => {
    if (!chartRef.current || kline.length === 0) return;

    const chart = createChart(chartRef.current, {
      width: chartRef.current.clientWidth,
      height: chartRef.current.clientHeight,
    });

    const series = chart.addCandlestickSeries();
    series.setData(kline);

    const markers = signals.map((sig) => ({
      time: sig.time,
      position: sig.signal === 'buy' ? 'belowBar' : 'aboveBar',
      color: sig.signal === 'buy' ? 'green' : 'red',
      shape: sig.signal === 'buy' ? 'arrowUp' : 'arrowDown',
      text: sig.signal,
    }));
    series.setMarkers(markers);

    const handleResize = () => {
      chart.resize(chartRef.current.clientWidth, chartRef.current.clientHeight);
    };
    window.addEventListener('resize', handleResize);
    return () => {
      chart.remove();
      window.removeEventListener('resize', handleResize);
    };
  }, [kline, signals]);

  return <div ref={chartRef} style={{ width: '100%', height: '100%' }} />;
};

export default KLineChart;
