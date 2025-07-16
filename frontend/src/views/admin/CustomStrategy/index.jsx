import React, { useEffect, useState } from 'react';
import axios from 'axios';
import {
  Box,
  Button,
  Card,
  HStack,
  Heading,
  Input,
  Select,
  Spinner,
  Stat,
  StatLabel,
  StatNumber,
  Text,
  VStack,
  SimpleGrid,
  CardBody,
} from '@chakra-ui/react';

const api = 'http://localhost:8888/api';

export default function CustomStrategy() {
  const [entryDict, setEntryDict] = useState({});
  const [exitDict, setExitDict] = useState({});
  const [entryIndicators, setEntryIndicators] = useState([]);
  const [exitIndicators, setExitIndicators] = useState([]);
  const [entryMode, setEntryMode] = useState('and');
  const [exitMode, setExitMode] = useState('or');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  // ✅ 載入所有可用指標分類
  useEffect(() => {
    const loadIndicators = async () => {
      try {
        const { data } = await axios.get(`${api}/available_indicators/`);
        setEntryDict(data.entry);
        setExitDict(data.exit);
      } catch (err) {
        console.warn('❗ 指標清單載入失敗：', err.message);
      }
    };

    loadIndicators();
  }, []);

  // ✅ 抓取 schema + 預設參數
  const fetchSchema = async (group, category, name) => {
    try {
      const res = await axios.get(`${api}/indicator_schema`, {
        params: { group, category, name },
      });
      const schema = res.data;
      const params = Object.fromEntries(
        Object.entries(schema).map(([k, v]) => [k, v.default]),
      );
      return { schema, params };
    } catch (err) {
      return { schema: {}, params: {} };
    }
  };

  // ✅ 更新指標內容
  const updateIndicator = async (
    group,
    index,
    field,
    value,
    indicators,
    setIndicators,
    dict,
  ) => {
    const updated = [...indicators];
    updated[index] = { ...updated[index], [field]: value };

    if (field === 'category') {
      const category = value;
      const name = dict[category]?.[0];
      if (!name) return;
      const { schema, params } = await fetchSchema(group, category, name);
      updated[index] = {
        category,
        name,
        schema,
        params,
      };
    }

    if (field === 'name') {
      const category = updated[index].category;
      const name = value;
      const { schema, params } = await fetchSchema(group, category, name);
      updated[index] = {
        ...updated[index],
        name,
        schema,
        params,
      };
    }

    setIndicators(updated);
  };

  const updateParam = (index, key, value, indicators, setIndicators) => {
    const updated = [...indicators];
    const updatedParams = { ...updated[index].params, [key]: Number(value) };
    updated[index] = { ...updated[index], params: updatedParams };
    setIndicators(updated);
  };

  const addIndicator = (group, dict, indicators, setIndicators) => {
    const category = Object.keys(dict);
    const name = dict[category];
    fetchSchema(group, category, name).then(({ schema, params }) => {
      setIndicators([
        ...indicators,
        {
          category,
          name,
          schema,
          params,
        },
      ]);
    });
  };

  const removeIndicator = (group, index) => {
    if(group === "entry") {
      const updated = [...entryIndicators];
      updated.splice(index, 1);
      setEntryIndicators(updated);
    }
    else if (group === 'exit') {
      const updated = [...exitIndicators];
      updated.splice(index, 1);
      setExitIndicators(updated);
    }
  }

  const handleRun = async () => {
    const payload = {
      entry_indicators: entryIndicators.map(({ category, name, params }) => ({
        category,
        name,
        params,
      })),
      exit_indicators: exitIndicators.map(({ category, name, params }) => ({
        category,
        name,
        params,
      })),
      entry_mode: entryMode,
      exit_mode: exitMode,
    };
    setLoading(true);
    try {
      const res = await axios.post(`${api}/customstrategy/`, payload);
      setResult({
        ...res.data,
        entry_indicators: payload.entry_indicators,
        exit_indicators: payload.exit_indicators,
      });
    } catch (err) {
      alert('🚫 執行回測時出錯！');
    } finally {
      setLoading(false);
      resetToInitial();
    }
  };
  const resetToInitial = () => {
    setEntryIndicators([]);
    setExitIndicators([]);
    setEntryMode('and');
    setExitMode('or');
  };

  const renderIndicators = (group, indicators, setIndicators, dict) => (
    <VStack align="stretch" spacing={4}>
      {indicators.map((ind, i) => (
        <Card key={i} p={3} bg="gray.100" position="relative" borderRadius="lg">
          <Button size="xs" colorScheme="red" position="absolute" top="1" right="1" borderRadius="full" transform="translate(25%, -25%)" zIndex="1" onClick={() => removeIndicator(group, i)}>
            ✕
          </Button>
          <Select
            placeholder="選擇類別"
            value={ind.category || ''}
            onChange={(e) =>
              updateIndicator(
                group,
                i,
                'category',
                e.target.value,
                indicators,
                setIndicators,
                dict,
              )
            }
          >
            {Object.keys(dict).map((cat) => (
              <option key={cat} value={cat}>
                {cat}
              </option>
            ))}
          </Select>

          <Select
            placeholder="選擇指標"
            value={ind.name || ''}
            onChange={(e) =>
              updateIndicator(
                group,
                i,
                'name',
                e.target.value,
                indicators,
                setIndicators,
                dict,
              )
            }
          >
            {(dict[ind.category] || []).map((name) => (
              <option key={name} value={name}>
                {name}
              </option>
            ))}
          </Select>

          {Object.entries(ind.schema || {}).map(([key, cfg]) => (
            <HStack key={key}>
              <Text>{key}</Text>
              <Input
                type="number"
                value={ind.params?.[key] ?? ''}
                onChange={(e) =>
                  updateParam(i, key, e.target.value, indicators, setIndicators)
                }
              />
            </HStack>
          ))}
        </Card>
      ))}
      <Button
        onClick={() => addIndicator(group, dict, indicators, setIndicators)}
      >
        ➕ 加入一個指標
      </Button>
      console.log("🔥 schema for indicator:", ind.name, ind.schema);
    </VStack>
  );

  return (
    <Box mt={20} p={6}>
      <SimpleGrid columns={2} spacing={10}>
        <Box>
          <Heading size="md" mb={2}>
            進場邏輯（Entry）
          </Heading>
          <Select
            value={entryMode}
            onChange={(e) => setEntryMode(e.target.value)}
          >
            <option value="and">AND</option>
            <option value="or">OR</option>
          </Select>
          {renderIndicators(
            'entry',
            entryIndicators,
            setEntryIndicators,
            entryDict,
          )}
        </Box>

        <Box>
          <Heading size="md" mb={2}>
            出場邏輯（Exit）
          </Heading>
          <Select
            value={exitMode}
            onChange={(e) => setExitMode(e.target.value)}
          >
            <option value="and">AND</option>
            <option value="or">OR</option>
          </Select>
          {renderIndicators(
            'exit',
            exitIndicators,
            setExitIndicators,
            exitDict,
          )}
        </Box>
      </SimpleGrid>

      <Button mt={8} colorScheme="teal" onClick={handleRun} isLoading={loading}>
        🚀 執行回測
      </Button>

      {result && (
        <Box mt={10}>
          <Heading size="md" mb={4}>
            🧭 本次使用的指標
          </Heading>

          <SimpleGrid mb={10} columns={2} spacing={10}>
            {/* 左邊：進場指標 */}
            <Box>
              <Text fontWeight="bold">📈 進場指標（Entry）:</Text>
              <VStack align="start" pl={4} mt={2}>
                {result?.entry_indicators?.map((ind, i) => (
                  <Card bg="purple.100" key={`entry-${i}`}>
                    <CardBody>
                      <Text fontWeight="bold" fontSize={'2xl'}>
                        {ind.name}
                      </Text>
                      <Box>
                        {Object.entries(ind.params).map(([key, value]) => (
                          <Text key={key}>
                            {' '}
                            {key}: {value}
                          </Text>
                        ))}
                      </Box>
                    </CardBody>
                  </Card>
                ))}
              </VStack>
            </Box>

            {/* 右邊：出場指標 */}
            <Box>
              <Text fontWeight="bold">📉 出場指標（Exit）:</Text>
              <VStack align="start" pl={4} mt={2}>
                {result?.exit_indicators?.map((ind, i) => (
                  <Card bg="purple.100" key={`entry-${i}`}>
                    <CardBody>
                      <Text fontWeight="bold" fontSize={'2xl'}>
                        {ind.name}
                      </Text>
                      <Box>
                        {Object.entries(ind.params).map(([key, value]) => (
                          <Text key={key}>
                            {' '}
                            {key}: {value}
                          </Text>
                        ))}
                      </Box>
                    </CardBody>
                  </Card>
                ))}
              </VStack>
            </Box>
          </SimpleGrid>
          <Heading size="md" mb={4}>
            📊 回測結果
          </Heading>
          <SimpleGrid columns={2} spacing={6}>
            <Stat>
              <StatLabel>初始資金</StatLabel>
              <StatNumber>${result.start_value}</StatNumber>
            </Stat>
            <Stat>
              <StatLabel>最終資金</StatLabel>
              <StatNumber>${result.final_value}</StatNumber>
            </Stat>
            <Stat>
              <StatLabel>年化報酬率</StatLabel>
              <StatNumber>{result.cagr}%</StatNumber>
            </Stat>
            <Stat>
              <StatLabel>Sharpe Ratio</StatLabel>
              <StatNumber>{result.sharpe}</StatNumber>
            </Stat>
            <Stat>
              <StatLabel>最大回檔</StatLabel>
              <StatNumber>{result.max_drawdown}%</StatNumber>
            </Stat>
          </SimpleGrid>
          <Box mt={4}>
            <img src={result.chart} alt="績效曲線" />
            <img src={result.drawdown_chart} alt="回檔圖" />
          </Box>
        </Box>
      )}
    </Box>
  );
}
