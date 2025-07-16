import { useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import axios from 'axios';
import { Box, Heading, Text, Spinner } from '@chakra-ui/react';
import {format} from 'date-fns';
import './BlogArticle.css';

export default function ArticleDetail() {
  const { id } = useParams(); 
  const [article, setArticle] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios
      .get(`http://140.116.214.140:8888/api/blog/${id}/`)
      .then((res) => setArticle(res.data))
      .catch((err) => console.error('載入文章失敗', err))
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) return <Spinner />;
  if (!article) return <Text>找不到文章</Text>;
  return (
    <Box mt="20" p="6">
      <Heading mb="4">{article.title}</Heading>
      <Text fontSize="sm" color="gray.500" mb="4">
        發佈時間：{format(new Date(article.created_at), 'yyyy-MM-dd HH:mm:ss')}
      </Text>
      <Box
        className="article-content"
        dangerouslySetInnerHTML={{ __html: article.content }}
      />
    </Box>
  );
}
