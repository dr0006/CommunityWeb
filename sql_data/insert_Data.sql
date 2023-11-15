/*
  2023-10-29 15:48
  用户: FxDr
  服务器: FXX-LEGION
  数据库: community_web
  应用程序: CommunityWeb 
*/
-- 村庄信息插入测试数据
INSERT INTO community_web.excellentcase_villageinfo (province, population, resources, industry, terrain, village_size,
                                                     avg_income, village_name)
VALUES ('湖南省', 12000000, '丰富的农产品和矿产资源', '农业和矿业', '丘陵地形', '中等规模', 48000.00, 'Village A'),
       ('广东省', 18000000, '发达的制造业和商业资源', '制造业和服务业', '平原地形', '大规模', 60000.00, 'Village B'),
       ('四川省', 15000000, '丰富的水资源和农业资源', '农业和水产业', '山地地形', '中等规模', 55000.00, 'Village C'),
       ('浙江省', 10000000, '发达的信息技术和制造业资源', '信息技术和制造业', '沿海地形', '中等规模', 52000.00,
        'Village D'),
       ('河北省', 13000000, '丰富的农业和煤炭资源', '农业和煤炭产业', '平原地形', '中等规模', 50000.00, 'Village E');


# 优秀案例的插入测试数据
INSERT INTO excellentcase_excellentcase (title, experience, village_info_id, category)
VALUES ('产业振兴案例1', '这是一个关于产业振兴的经验描述。', 1, 'industrial'),
       ('人才振兴案例1', '这是一个关于人才振兴的经验描述。', 2, 'talent'),
       ('文化振兴案例1', '这是一个关于文化振兴的经验描述。', 3, 'cultural'),
       ('生态振兴案例1', '这是一个关于生态振兴的经验描述。', 4, 'ecological'),
       ('组织振兴案例1', '这是一个关于组织振兴的经验描述。', 5, 'organizational');
