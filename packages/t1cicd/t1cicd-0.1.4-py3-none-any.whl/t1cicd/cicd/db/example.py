# from uuid import UUID
#
# from src.cicd.db.context.pipeline import PipelineCreateContext
# from src.cicd.db.db import DB
# from src.cicd.db.transaction.pipeline import PipelineTransaction
# from src.cicd.parser.pipeline import ParsedPipeline

# async def example_usage():
#     # db init
#     await DB.init(DBConfig.from_env())
#
#     # create a new pipeline
#
#     pipeline_repo = DB.get_repository(PipelineRepository)
#     new_pipeline = await pipeline_repo.create(
#         PipelineCreate(
#             git_branch="feature/new-feature",
#             git_hash="abc123def456",
#             git_comment="Add new feature",
#             pipeline_name="pipeline_name",
#             status=PipelineStatus.PENDING,
#         )
#     )
#     print(f"Created pipeline: {new_pipeline.id}")
#     new_pipeline.status = PipelineStatus.SUCCESS
#     update_pipeline = await pipeline_repo.update(new_pipeline)
#     print("Updated pipeline, expected status to be success")
#     print(update_pipeline)
#
#     # create stages for the pipeline
#     stage_repo = DB.get_repository(StageRepository)
#     stage1 = await stage_repo.create(
#         StageCreate(
#             stage_name="stage1",
#             pipeline_id=new_pipeline.id,
#             stage_order=1,
#         )
#     )
#     await stage_repo.create(
#         StageCreate(
#             stage_name="stage2",
#             pipeline_id=new_pipeline.id,
#             stage_order=2,
#         )
#     )
#     stage1.status = StageStatus.FAILED
#     await stage_repo.update(stage1)
#     print("Update stage, expected status to be failed")
#     new_stage = await stage_repo.get(stage1.id)
#     print(new_stage)
#
#     result = await pipeline_repo.get(new_pipeline.id)
#     print(result)
#
#     job_repo = DB.get_repository(JobRepository)
#     job1 = await job_repo.create(
#         JobCreate(
#             stage_id=stage1.id,
#             job_name="job1",
#             job_order=1,
#         )
#     )
#     print(f"Created job: {job1.id}")
#     job1.status = JobStatus.SUCCESS
#     await job_repo.update(job1)
#     print("Update job, expected status to be success")
#     new_job = await job_repo.get(job1.id)
#     print(new_job)
#     job2 = await job_repo.create(
#         JobCreate(
#             stage_id=stage1.id,
#             job_name="job2",
#             job_order=2,
#         )
#     )
#     print(f"Created job: {job2.id}")
#
#     stage_result = await stage_repo.get(stage1.id)
#     print(stage_result)
#
#     # add artifacts to the job1
#     artifact_repo = DB.get_repository(ArtifactRepository)
#     await artifact_repo.create(
#         ArtifactCreate(
#             job_id=job1.id,
#             file_path="artifact1",
#             file_size=100,
#         )
#     )
#     artifact2 = await artifact_repo.create(
#         ArtifactCreate(
#             job_id=job1.id,
#             file_path="artifact2",
#             file_size=200,
#             expiry_date=datetime.now(),
#         )
#     )
#
#     print(f"Created artifact: {artifact2.id}")
#     # update artifact
#     artifact2.expiry_date = datetime(2023, 1, 1, 12, 0, 0)
#     await artifact_repo.update(artifact2)
#     result = await artifact_repo.get(artifact2.id)
#     print(
#         result,
#         f"Updated artifact: {artifact2.id}, expected expiry date to be 2023-01-01 12:00:00",
#     )
#
#     # query artifacts for job1
#
#     job1 = await job_repo.get(job1.id)
#     print(job1)
#     # cleanup
#
#     await pipeline_repo.delete(new_pipeline.id)
#     print("Deleted pipeline")
#
#     # close db
#     await DB.close()


# async def main():
#     await create_pipeline_example()


# async def create_pipeline_example():
#     await DB.init(DBConfig.from_env())
#     # replace this with pipeline file
#     parser = YAMLParser("pipeline.yml")
#     parsed_pipeline = parser.parse()
#     context = PipelineCreateContext(
#         git_branch="feature/new-feature",
#         git_hash="abc123def456",
#         git_comment="Add new feature",
#         repo_url="github.com/owner/repo",
#     )
#     pipeline_transaction = DB.get_transaction(PipelineTransaction)
#     pipeline_id, run_id = await pipeline_transaction.create_new_pipeline(
#         parsed_pipeline, context
#     )
#     print(f"Created pipeline: {pipeline_id}, {run_id}")
#     await DB.close()

#
# async def create_pipeline(
#     parsed_pipeline: ParsedPipeline,
#     git_branch: str,
#     git_hash: str,
#     git_comment: str = "",
#     repo_url: str = "",
# ) -> tuple[UUID, int]:
#     context = PipelineCreateContext(
#         git_branch=git_branch,
#         git_hash=git_hash,
#         git_comment=git_comment,
#         repo_url=repo_url,
#     )
#     pipeline_transaction = DB.get_transaction(PipelineTransaction)
#     pipeline_id, run_id = await pipeline_transaction.create_new_pipeline(
#         parsed_pipeline, context
#     )
#     print(f"Created pipeline: {pipeline_id}")
#     return pipeline_id, run_id


# if __name__ == "__main__":
#     asyncio.run(main())
#
#
# def main():
#     asyncio.run(example_usage())
