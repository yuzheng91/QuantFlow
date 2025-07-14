// CustomStrategy.jsx  (React + Chakra UI)
import axios from "axios";

import React, { useEffect, useState } from 'react';
import {
  Box,
  Button,
  Card,
  CardBody,
  VStack,
  HStack,
  Heading,
  Select,
  Text,
  Spinner,
  Input,
  SimpleGrid,
  StatLabel,
  Stat,
  StatNumber,
} from '@chakra-ui/react';

const api = 'http://127.0.0.1:8000/api';

export default function CustomStrategy() {
  // 指標清單 (分類後)
  const [entryDict, setEntryDict] = useState({});
  const [exitDict, setExitDict] = useState({});

  // 目前選擇
  const [entryCat, setEntryCat] = useState('');
  const [entryName, setEntryName] = useState('');
  const [exitCat, setExitCat] = useState('');
  const [exitName, setExitName] = useState('');

  // schema 與參數
  const [entrySchema, setEntrySchema] = useState({});
  const [exitSchema, setExitSchema] = useState({});
  const [entryParams, setEntryParams] = useState({});
  const [exitParams, setExitParams] = useState({});

  // 回測結果
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const [exitParamsConfirmed, setExitParamsConfirmed] = useState(false);
  const [entryParamsConfirmed, setEntryParamsConfirmed] = useState(false);

  // ─── 取得分類指標清單 ───
  useEffect(() => {
    axios.get(`${api}/available_indicators/`)
      .then(({ data }) => {
        const { entry, exit } = data;
        setEntryDict(entry);
        setExitDict(exit);

        const firstEntryCat = Object.keys(entry)[0];
        const firstEntry = entry[firstEntryCat][0];
        const firstExitCat = Object.keys(exit)[0];
        const firstExit = exit[firstExitCat][0];

        setEntryCat(firstEntryCat);
        setEntryName(firstEntry);
        setExitCat(firstExitCat);
        setExitName(firstExit);
      })
      .catch((err) => console.error("Error loading indicators:", err));
  }, []);

  // ─── 抓 entry schema ───
  useEffect(() => {
    if (!entryCat || !entryName) return;
    axios.get(`${api}/indicator_schema`, {
      params: {
        group: "entry",
        category: entryCat,
        name: entryName,
      }
    })
      .then(({ data }) => {
        setEntrySchema(data);
        setEntryParams(
          Object.fromEntries(
            Object.entries(data).map(([k, v]) => [k, v.default])
          )
        );
      })
      .catch((err) => console.error("Error loading entry schema:", err));
  }, [entryCat, entryName]);

  // ─── 抓 exit schema ───
  useEffect(() => {
    if (!exitCat || !exitName) return;
    axios.get(`${api}/indicator_schema`, {
      params: {
        group: "exit",
        category: exitCat,
        name: exitName,
      }
    })
      .then(({ data }) => {
        setExitSchema(data);
        setExitParams(
          Object.fromEntries(
            Object.entries(data).map(([k, v]) => [k, v.default])
          )
        );
      })
      .catch((err) => console.error("Error loading exit schema:", err));
  }, [exitCat, exitName]);

  // ─── 送出回測 ───
  const handleRun = async () => {
    setLoading(true);
    setResult(null);
    const payload = {
      entry_category: entryCat,
      entry_name: entryName,
      exit_category: exitCat,
      exit_name: exitName,
      entry_params: entryParams,
      exit_params: exitParams,
    };
    try {
      const res = await fetch(`${api}/customstrategy/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      setResult(await res.json());
      setEntryParamsConfirmed(false);
      setExitParamsConfirmed(false);
    } catch (e) {
      alert(e.message);
    } finally {
      setLoading(false);
    }
  };

  // ─── 產生參數欄位 ───
  const renderParams = (schema, params, setParams, confirmed = false) => {
    return (
      <VStack align="stretch" spacing={3}>
        {Object.entries(schema).map(([key, cfg]) => (
          <HStack key={key}>
            <Text w="100px">{key}=</Text>
            {confirmed ? (
              <Text>{params[key]}</Text>
            ) : (
              <Input
                size="sm"
                type="number"
                min={cfg.min}
                max={cfg.max}
                value={params[key]}
                onChange={(e) =>
                  setParams({ ...params, [key]: Number(e.target.value) })
                }
              />
            )}
          </HStack>
        ))}
      </VStack>
    );
  };

  // ─── 畫面 ───
  return (
    <VStack spacing={8} align="stretch" px={6}>
      <HStack align="start" spacing={10} pt="100px" px={6}>
        {/* 左側設定 */}
        <VStack flex={1} align="stretch">
          <Heading size="md">Strategy Settings</Heading>

          {/* Entry 類別 */}
          <Card p={4} bg="purple.100" borderRadius="md">
            <Box>
              <Text m={1} fontWeight="bold">
                Entry Type：
              </Text>
              <Select
                bg="purple.50"
                value={entryCat}
                onChange={(e) => {
                  const cat = e.target.value;
                  setEntryCat(cat);
                  setEntryName(entryDict[cat][0] || '');
                  setEntryParamsConfirmed(false);
                }}
              >
                {Object.keys(entryDict)
                  .sort()
                  .map((cat) => (
                    <option key={cat} value={cat}>
                      {cat}
                    </option>
                  ))}
              </Select>
            </Box>
          </Card>

          {/* Entry 指標 */}
          <Card p={4} bg="purple.100" borderRadius="md">
            <Box>
              <Text m={1} fontWeight="bold">
                Entry Indicators：
              </Text>
              <Select
                bg="purple.50"
                value={entryName}
                onChange={(e) => {
                  setEntryName(e.target.value);
                  setEntryParamsConfirmed(false);
                }}
              >
                {(entryDict[entryCat] || []).map((ind) => (
                  <option key={ind} value={ind}>
                    {ind}
                  </option>
                ))}
              </Select>
            </Box>
          </Card>
          {entryName && !entryParamsConfirmed && (
            <>
              {renderParams(entrySchema, entryParams, setEntryParams)}
              <Button
                mt={2}
                size="sm"
                colorScheme="purple"
                onClick={() => setEntryParamsConfirmed(true)}
              >
                Confirmed
              </Button>
            </>
          )}

          {/* Exit 類別 */}
          <Card p={4} bg="purple.100" borderRadius="md">
            <Box>
              <Text m={1} fontWeight="bold">
                Exit Type：
              </Text>
              <Select
                bg="purple.50"
                value={exitCat}
                onChange={(e) => {
                  const cat = e.target.value;
                  setExitCat(cat);
                  setExitName(exitDict[cat][0] || '');
                  setExitParamsConfirmed(false);
                }}
              >
                {Object.keys(exitDict)
                  .sort()
                  .map((cat) => (
                    <option key={cat} value={cat}>
                      {cat}
                    </option>
                  ))}
              </Select>
            </Box>
          </Card>

          {/* Exit 指標 */}
          <Card p={4} bg="purple.100" borderRadius="md">
            <Box>
              <Text m={1} fontWeight="bold">
                Exit Indicators：
              </Text>
              <Select
                bg="purple.50"
                value={exitName}
                onChange={(e) => {
                  setExitName(e.target.value);
                  setExitParamsConfirmed(false);
                }}
              >
                {(exitDict[exitCat] || []).map((ind) => (
                  <option key={ind} value={ind}>
                    {ind}
                  </option>
                ))}
              </Select>
            </Box>
          </Card>
          {exitName && !exitParamsConfirmed && (
            <>
              {renderParams(exitSchema, exitParams, setExitParams)}
              <Button
                mt={2}
                size="sm"
                colorScheme="purple"
                onClick={() => setExitParamsConfirmed(true)}
              >
                Confirmed
              </Button>
            </>
          )}

          <Button
            m={6}
            colorScheme="purple"
            onClick={handleRun}
            disabled={loading}
          >
            {loading && <Spinner size="sm" mr={2} />}
            Excute Backtest
          </Button>
        </VStack>

        {/* 右側結果 */}
        <VStack flex={1} align="stretch">
          <Box p={4} bg="gray.50" borderRadius="md">
            <Heading size="md">Backtest Result</Heading>
            {loading && <Text>回測中…</Text>}
            {result && (
              <Box p={4} bg="gray.50" borderRadius="md">
                <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={6}>
                  <Stat>
                    <StatLabel>💰 Start Value：</StatLabel>
                    <StatNumber>${result.start_value.toFixed(2)}</StatNumber>
                  </Stat>
                  <Stat>
                    <StatLabel>💰 Final Value：</StatLabel>
                    <StatNumber>${result.final_value.toFixed(2)}</StatNumber>
                  </Stat>
                  <Stat>
                    <StatLabel>📊 CAGR：</StatLabel>
                    <StatNumber>{result.cagr.toFixed(2)}%</StatNumber>
                  </Stat>
                  <Stat>
                    <StatLabel>📉 Maximum Drawdown：</StatLabel>
                    <StatNumber>{result.max_drawdown.toFixed(2)}%</StatNumber>
                  </Stat>
                  <Stat>
                    <StatLabel>📆 Drawdown Duration：</StatLabel>
                    <StatNumber>{result.drawdown_duration} days</StatNumber>
                  </Stat>
                  <Stat>
                    <StatLabel>⚖️ Sharpe Ratio：</StatLabel>
                    <StatNumber>{result.sharpe.toFixed(2)}</StatNumber>
                  </Stat>
                </SimpleGrid>
              </Box>
            )}
          </Box>
        </VStack>
      </HStack>
      {result?.chart && (
        <Box bg="white" p={4} borderRadius="md" shadow="sm">
          <Heading size="sm" mb={2}>
            Strategy vs Benchmark
          </Heading>
          <img
            src={result.chart}
            alt="strategy vs benchmark"
            style={{ width: '100%', maxHeight: 400, objectFit: 'contain' }}
          />
        </Box>
      )}
      {result?.drawdown_duration && (
        <Box bg="white" p={4} borderRadius="md" shadow="sm">
          <Heading size="sm" mb={2}>
            Drawdown Comparison
          </Heading>
          <img
            src={result.drawdown_chart}
            alt="Drawdown Comparison"
            style={{ width: '100%', maxHeight: 400, objectFit: 'contain' }}
          />
        </Box>
      )}
    </VStack>
  );
}
