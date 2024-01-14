import { useEffect, useState } from "preact/hooks"
import useCityPromotion from "./useCityPromotion";

export default function useCityFilter({ sourceList, defaultValue }) {
    const [ filteredList, setFilteredList ] = useState([]);
    const [ cityFilter, setCityFilter ] = useState(defaultValue);
    const { cities, fetchCitiesWeekplan } = useCityPromotion();

    useEffect(() => {
        if (cityFilter === "" || cityFilter === null) {
            setFilteredList(sourceList);
            return
        }
        let newWp = sourceList.filter((e) => {
            return e.city === cityFilter
        });
        setFilteredList([...newWp]);
    }, [ cityFilter, sourceList ]);

    const handleCityFilterChange = (event) => {
        setCityFilter(event.target.value);
    }

    return {
        filteredList: filteredList,
        cityFilter: cityFilter,
        setCityFilter: setCityFilter,
        handleCityFilterChange: handleCityFilterChange,
        cities: cities
    }
}