import { useEffect, useState } from "react";
import axios from "axios";
import {
  MdAddTask,
  MdAttachMoney,
  MdBarChart,
  MdFileCopy,
  MdTrendingUp,
  MdTrendingDown,
} from "react-icons/md";
import {
  Box,
  Stat,
  StatLabel,
  StatNumber,
  Text,
  Heading,
  VStack,
  SimpleGrid,
  useColorModeValue,
  HStack,
  Center,
  Icon
} from "@chakra-ui/react";
import IconBox from "components/icons/IconBox";

function PerformanceBlock() {
  const brandColor = useColorModeValue("brand.500", "white");
  const boxBg = useColorModeValue("secondaryGray.300", "whiteAlpha.100");
  const [metricsList, setMetricsList] = useState([]);
  const bg = useColorModeValue("white", "gray.700");

  useEffect(() => {
    axios.get("http://localhost:8000/api/fixedstrategy/").then((res) => {
      setMetricsList(res.data);
    });
  }, []);

  if (!metricsList.length) return <Text>正在載入績效資料...</Text>;

  return (
    <VStack align="stretch" spacing={6}>
      {metricsList.map((metrics, index) => {
        const isProfit = metrics.final_value>=metrics.start_value;
        const iconColor = isProfit ? "green.400" : "red.400";
        return(
          <Box
            key={index}
            bg={bg}
            p={6}
            borderRadius="xl"
            shadow="md"
          >
            <Heading size="md" mb={4}>
              策略：{metrics.name}
            </Heading>
            <SimpleGrid columns={[1, 2, 3, 4, 5]} spacing={6}>
              <HStack align="start" spacing={4}>
                <Center
                  w="40px"
                  h="40px"
                  bg="purple.50"
                  borderRadius="full"
                >
                  <Icon as={MdAttachMoney} w={5} h={5} color="purple.400" />
                </Center>

                <Box>
                  <Text fontSize="sm" color="gray.400" fontWeight="medium">
                    Start Value
                  </Text>
                  <Text fontSize="xl" fontWeight="bold" color="gray.800">
                    ${metrics.start_value}
                  </Text>
                </Box>
              </HStack>
              <HStack align="start" spacing={4}>
                <Center
                  w="40px"
                  h="40px"
                  bg="purple.50"
                  borderRadius="full"
                >
                  <Icon as={MdAttachMoney} w={5} h={5} color={iconColor}/>
                </Center>

                <Box>
                  <Text fontSize="sm" color="gray.400" fontWeight="medium">
                    Final Value
                  </Text>
                  <Text fontSize="xl" fontWeight="bold" color={iconColor}>
                    ${metrics.final_value}
                  </Text>
                </Box>
              </HStack>
              <HStack align="start" spacing={4}>
                <Center
                  w="40px"
                  h="40px"
                  bg="purple.50"
                  borderRadius="full"
                >
                  <Icon as={MdBarChart} w={5} h={5} color={iconColor} />
                </Center>

                <Box>
                  <Text fontSize="sm" color="gray.400" fontWeight="medium">
                    CAGR
                  </Text>
                  <Text fontSize="xl" fontWeight="bold" color={iconColor}>
                    {metrics.cagr}%
                  </Text>
                </Box>
              </HStack>
              <HStack align="start" spacing={4}>
                <Center
                  w="40px"
                  h="40px"
                  bg="purple.50"
                  borderRadius="full"
                >
                  <Icon as={MdTrendingDown} w={5} h={5} color="red.400" />
                </Center>

                <Box>
                  <Text fontSize="sm" color="gray.400" fontWeight="medium">
                    Sharpe
                  </Text>
                  <Text fontSize="xl" fontWeight="bold" color="red.400">
                    {metrics.sharpe}
                  </Text>
                </Box>
              </HStack>
              <HStack align="start" spacing={4}>
                <Center
                  w="40px"
                  h="40px"
                  bg="purple.50"
                  borderRadius="full"
                >
                  <Icon as={MdTrendingDown} w={5} h={5} color="red.400" />
                </Center>

                <Box>
                  <Text fontSize="sm" color="gray.400" fontWeight="medium">
                    Max Drawdown
                  </Text>
                  <Text fontSize="xl" fontWeight="bold" color="red.400">
                    {metrics.max_drawdown}%
                  </Text>
                </Box>
              </HStack>
            </SimpleGrid>
          </Box>
        );
      })}
    </VStack>
  );
}

export default PerformanceBlock;
