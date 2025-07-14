import { Box, Heading, Text, Button } from '@chakra-ui/react';
import { useNavigate } from 'react-router-dom';

const ArticleCard = ({ article }) => {
  const navigate = useNavigate();

  return (
    <Box p={5} shadow="md" borderWidth="1px" borderRadius="lg">
      <Heading fontSize="xl">{article.title}</Heading>
      <Text mt={2} dangerouslySetInnerHTML={{ __html: article.summary }} />
      <Button mt={20} colorScheme="purple" onClick={() => navigate(`/admin/blog/${article.id}`)}>
        繼續閱讀
      </Button>
    </Box>
  );
};

export default ArticleCard;
