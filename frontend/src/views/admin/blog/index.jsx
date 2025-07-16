import { useEffect, useState } from 'react';
import axios from 'axios';
import {
  Box,
  Heading,
  Text,
  Spinner,
  VStack,
  HStack,
  Button,
  Card,
} from '@chakra-ui/react';
import ArticleCard from './components/articlecard';

const api = 'http://140.116.214.140:8888/api';

export default function Blog() {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [nextPage, setNextPage] = useState(null);
  const [prevPage, setPrevPage] = useState(null);
  const [currentPageUrl, setCurrentPageUrl] = useState(
    'http://140.116.214.140:8888/api/blog/',
  );
  const [categories, setCategories] = useState([]);
  const [currentCategory, setCurrentCategory] = useState('All');
  const latestArticle = articles.length > 0 ? articles[0] : null;
  const otherArticles = articles.slice(1);
  useEffect(() => {
    axios
      .get(currentPageUrl)
      .then((res) => {
        setArticles(res.data.results); // 當前這一頁的文章資料
        setNextPage(res.data.next); // 下一頁網址
        setPrevPage(res.data.previous); // 上一頁網址
      })
      .finally(() => {
        setLoading(false);
      });
  }, [currentPageUrl]);

  useEffect(() => {
    axios.get('http://140.116.214.140:8888/api/categories/').then((res) => {
      setCategories(['All', ...res.data.results.map((cat) => cat.name)]);
    });
  }, []);

  if (loading) return <Spinner />;

  return (
    <Box mt="20" px="4">
      {latestArticle && (
        <Box m="10">
          <Heading mb="4" size="md" color="purple.600">
            🆕 最新發布
          </Heading>
          <ArticleCard article={latestArticle} />
        </Box>
      )}
      <HStack mb="4" spacing={3}>
        {categories.map((cat) => (
          <Button
            key={cat}
            onClick={() => {
              setCurrentCategory(cat);
              console.log('你點了分類：', cat);
              const baseUrl = 'http://140.116.214.140:8888/api/blog/';
              const url =
                cat === 'All'
                  ? baseUrl
                  : `${baseUrl}?category=${encodeURIComponent(cat)}`;
              console.log('實際 API URL：', url);
              setCurrentPageUrl(url); // ✅ 更新文章 API URL
              setLoading(true);
            }}
            variant={cat === currentCategory ? 'solid' : 'outline'}
            colorScheme="purple"
          >
            {cat}
          </Button>
        ))}
      </HStack>
      <VStack align="stretch" spacing={4}>
        {articles.map((article) => (
          <ArticleCard key={article.id} article={article} />
        ))}
      </VStack>
      {/* 分頁按鈕區塊 */}
      <Box mt="6" display="flex" justifyContent="center" gap="4">
        <Button
          onClick={() => {
            const url =
              currentCategory === 'All'
                ? prevPage
                : `${prevPage}&category=${currentCategory}`;
            setCurrentPageUrl(url);
            setLoading(true);
          }}
          disabled={!prevPage}
          style={{
            padding: '8px 16px',
            backgroundColor: prevPage ? '#3182ce' : '#a0aec0',
            color: 'white',
            border: 'none',
            borderRadius: '6px',
            cursor: prevPage ? 'pointer' : 'not-allowed',
          }}
        >
          上一頁
        </Button>

        <Button
          onClick={() => {
            const url =
              currentCategory === 'All'
                ? nextPage
                : `${nextPage}&category=${currentCategory}`;
            setCurrentPageUrl(url);
            setLoading(true);
          }}
          disabled={!nextPage}
          style={{
            padding: '8px 16px',
            backgroundColor: nextPage ? '#3182ce' : '#a0aec0',
            color: 'white',
            border: 'none',
            borderRadius: '6px',
            cursor: nextPage ? 'pointer' : 'not-allowed',
          }}
        >
          下一頁
        </Button>
      </Box>
    </Box>
  );
}
