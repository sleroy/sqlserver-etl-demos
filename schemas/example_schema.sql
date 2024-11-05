CREATE TABLE [dbo].[ExampleLargeTable](
	[CustomerId] [binary](16) NOT NULL,
	[IpId] [nchar](16) NOT NULL,
	[CustIntId] [nvarchar](10) NOT NULL,
	[LoadStatusId] [bigint] NOT NULL,
	[CustomerIdInt] [bigint] IDENTITY(1,1) NOT NULL,
	[IsAnonymized] [bit] NULL,
 CONSTRAINT [PK_ExampleLargeTable_CustomerIdEffDtEndDt] PRIMARY KEY CLUSTERED 
(
	[CustomerId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
