import React from "react";

// Chakra imports
import { Flex, useColorModeValue, Text} from "@chakra-ui/react";

// Custom components
import { HorizonLogo } from "components/icons/Icons";
import { HSeparator } from "components/separator/Separator";

export function SidebarBrand() {
  //   Chakra color mode
  let logoColor = useColorModeValue("navy.700", "whilte");

  return (
    <Flex align='center' direction='column'>
      <Text fontSize="2xl" fontWeight="bold" color={logoColor} my="32px">
        量化交易策略平台
      </Text>

      <HSeparator mb='20px' />
    </Flex>
  );
}

export default SidebarBrand;
