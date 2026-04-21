class ESIndex:
    # 索引名模板（支持动态传入 knowledge_id）
    INDEX_NAME_TEMPLATE = "knowledge_slice_{knowledge_id}"

    # ES 索引配置（固定结构）
    INDEX_BODY = {
        "settings": {
            "number_of_shards": 3,
            "number_of_replicas": 1,
            "refresh_interval": "30s",
            "analysis": {
                "analyzer": {
                    "ik_max_word_analyzer": {
                        "type": "custom",
                        "tokenizer": "ik_max_word"
                    },
                    "ik_smart_analyzer": {
                        "type": "custom",
                        "tokenizer": "ik_smart"
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "slice_id": {"type": "long"},
                "document_id": {"type": "long"},
                "knowledge_id": {"type": "long"},
                "content": {
                    "type": "text",
                    "analyzer": "ik_max_word_analyzer",
                    "search_analyzer": "ik_smart_analyzer"
                },
                "sequence": {"type": "double"},
                "update_time": {
                    "type": "date",
                    "format": "yyyy-MM-dd HH:mm:ss"
                },
                "updater": {"type": "keyword"}
            }
        }
    }

    @classmethod
    def get_index_name(cls, knowledge_id: int) -> str:
        """
        动态生成索引名：knowledge_slice_123
        """
        return cls.INDEX_NAME_TEMPLATE.format(knowledge_id=knowledge_id)