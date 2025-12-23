export const profile = {
	fullName: 'Eva van Heese',
	title: 'PhD Candidate',
	institute: 'Amsterdam University Medical Centre, the Netherlands',
	author_name: 'Eva van Heese', // Author name to be highlighted in the papers section
	research_areas: [
  {
    title: 'MRI',
    description: 'Advanced MRI methods to study brain structure, function, and physiology in health and disease.',
    field: 'mri',
  },
  {
    title: 'Sleep and sleep disorders',
    description: 'Sleep disorders, with a focus on narcolepsy and other central disorders of hypersomnolence, REM sleep behaviour disorder, and the effects of sleep and sleep deprivation.',
    field: 'sleep',
  },
  {
    title: 'Neurodegeneration',
    description: 'MRI-based investigation of brain changes in neurodegenerative diseases, including Parkinson’s disease and dementia with Lewy bodies.',
    field: 'neurodegeneration',
  },
  {
    title: 'Brain clearance',
    description: 'MRI-based investigation of brain clearance processes at the intersection of sleep and neurodegeneration.',
    field: 'brain-clearance',
  },
  {
    title: 'Large, multi-site datasets',
  	description: 'Central role in coordinating international consortia, focussed on pooling imaging data to improve power, reproducibility, and diversity across datasets.',
  	field: 'multi-site-datasets',
  },
  {
    title: 'Open science',
    description: 'Promotion of open and reproducible research through transparent methods, open code, inclusive collaboration, and public outreach and teaching',
    field: 'open-science',
  },
],
}

// Set equal to an empty string to hide the icon that you don't want to display
export const social = {
	email: 'mailto:e.vanheese@amsterdamumc.nl',
	linkedin: '',
	x: '',
	bluesky: '',
	github: 'https://github.com/evavanheese',
	gitlab: '',
	scholar: 'https://scholar.google.com/citations?hl=en&view_op=list_works&user=JhpThRUAAAAJ',
	inspire: '',
	arxiv: '',
	orcid: 'https://orcid.org/0000-0002-1954-5014',
}

export const template = {
  website_url: 'https://evavanheese.github.io',
  menu_left: false,
  transitions: true,
  lightTheme: 'light',
  darkTheme: 'dark',
  excerptLength: 200,
  postPerPage: 5,
  base: '' // user site
}

export const seo = {
	default_title: 'Eva van Heese',
	default_description: '',
	default_image: '/images/eva-van-heese-picture.jpg',
}
