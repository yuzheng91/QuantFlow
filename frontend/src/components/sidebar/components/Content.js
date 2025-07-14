// chakra imports
import { Link, Box, Flex, Stack, Text, Image } from "@chakra-ui/react";
//   Custom components
import Brand from "components/sidebar/components/Brand";
import Links from "components/sidebar/components/Links";
import SidebarCard from "components/sidebar/components/SidebarCard";
import React from "react";

// FUNCTIONS

function SidebarContent(props) {
  const { routes } = props;
  // SIDEBAR
  return (
    <Flex direction='column' height='100%' pt='25px' px="16px" borderRadius='30px'>
      <Brand />
      <Stack direction='column' mb='auto' mt='8px'>
        <Box ps='20px' pe={{ md: "16px", "2xl": "1px" }}>
          <Links routes={routes} />
        </Box>
      </Stack>

      <Box mt='60px' mb='40px' borderRadius='30px' textAlign="center">
        <Link href="https://www.facebook.com/groups/138522979571148" isExternal>
          <Image
            src="https://upload.wikimedia.org/wikipedia/commons/5/51/Facebook_f_logo_%282019%29.svg"
            alt="Facebook"
            boxSize="30px"
            mx="auto"
            mb="10px"
          />
          <Text fontSize="sm" color="blue.500">追蹤我們的 Facebook</Text>
        </Link>
      </Box>
    </Flex>
  );
}

export default SidebarContent;
